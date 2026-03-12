"""
OpenRouter Agent for Todo AI Chatbot.

This module provides a lightweight agent that works with OpenRouter API.
OpenRouter offers FREE tier with access to multiple models (Qwen, Llama, etc.)
Perfect for cloud deployment!

Docs: https://openrouter.ai/docs
"""

import logging
import json
import re
import time
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

import httpx

from mcp_server.tools.task_tools import (
    add_task as mcp_add_task,
    list_tasks as mcp_list_tasks,
    complete_task as mcp_complete_task,
    delete_task as mcp_delete_task,
    update_task as mcp_update_task,
)
from mcp_server.context import create_mcp_context
from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Response from agent processing."""
    content: str
    tool_calls: List[Dict[str, Any]]
    conversation_id: Optional[str] = None


class OpenRouterTodoAgent:
    """
    OpenRouter-based agent for todo management.
    Works with free tier models like Qwen-2.5-7B-Instruct
    """

    def __init__(self, user_id: str):
        """
        Initialize the agent with user context.

        Args:
            user_id: The authenticated user's ID
        """
        self.user_id = user_id
        self._context = None
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        # Use Gemini 2.0 Flash Lite for fast, reliable responses
        self.model = "google/gemini-2.0-flash-lite-001"
        logger.info(f"OpenRouterTodoAgent initialized for user: {user_id}")
        logger.info(f"  Model: {self.model}")
        logger.info(f"  Base URL: {self.base_url}")

    def _get_context(self):
        """Get or create MCP context."""
        if self._context is None:
            self._context = create_mcp_context(user_id=self.user_id)
        return self._context

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return the result."""
        ctx = self._get_context()
        print(f'\n[TOOL CALL] Executing: {tool_name}')
        print(f'   Arguments: {arguments}')

        try:
            if tool_name == "add_task":
                result = mcp_add_task(ctx, title=arguments.get("title", ""))
            elif tool_name == "list_tasks":
                result = mcp_list_tasks(ctx, status=arguments.get("status", "all"))
            elif tool_name == "complete_task":
                result = mcp_complete_task(ctx, task_id=arguments.get("task_id", ""))
            elif tool_name == "delete_task":
                result = mcp_delete_task(ctx, task_id=arguments.get("task_id", ""))
            elif tool_name == "update_task":
                result = mcp_update_task(
                    ctx,
                    task_id=arguments.get("task_id", ""),
                    title=arguments.get("title"),
                    completed=arguments.get("completed"),
                )
            else:
                result = {"success": False, "error": f"Unknown tool: {tool_name}"}

            print(f'   [SUCCESS] Result: {result.get("success", False)}')
            return result

        except Exception as e:
            print(f'   [ERROR] {type(e).__name__}: {str(e)}')
            logger.error(f"Tool execution failed: {e}")
            return {"success": False, "error": str(e)}

    def _extract_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract tool call from AI response text."""
        # Pattern 1: [TOOL:tool_name]{"arg": "value"}
        pattern = r'\[TOOL:(\w+)\](\{[^}]+\})'
        match = re.search(pattern, text)

        if match:
            try:
                tool_name = match.group(1)
                args = json.loads(match.group(2))
                return {"name": tool_name, "arguments": args}
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse tool arguments: {match.group(2)}")
        
        # Pattern 2: Look for tool calls in any format
        # Check for delete_task
        if 'delete' in text.lower() and 'task' in text.lower():
            # Extract task name from quotes
            name_match = re.search(r'"([^"]+)"', text)
            if name_match:
                return {"name": "delete_task", "arguments": {"task_id": name_match.group(1)}}
        
        # Check for complete_task
        if 'complete' in text.lower() or 'mark' in text.lower():
            name_match = re.search(r'"([^"]+)"', text)
            if name_match:
                return {"name": "complete_task", "arguments": {"task_id": name_match.group(1)}}
        
        # Check for add_task
        if 'add' in text.lower() or 'create' in text.lower():
            name_match = re.search(r'"([^"]+)"', text)
            if name_match:
                return {"name": "add_task", "arguments": {"title": name_match.group(1)}}
        
        return None

    def process_message(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> AgentResponse:
        """Process a user message and generate an AI response."""
        print(f'\n[OPENROUTER AGENT] Processing message for user: {self.user_id}')
        print(f'   Message: "{message[:100]}..."')

        # Concise system prompt to reduce token usage
        system_prompt = """You are a helpful todo assistant.

Available tools (use EXACT format with square brackets):
[TOOL:add_task]{"title": "task name"}
[TOOL:list_tasks]{"status": "all|pending|completed"}
[TOOL:complete_task]{"task_id": "task name"}
[TOOL:delete_task]{"task_id": "task name"}
[TOOL:update_task]{"task_id": "task name", "title": "new title", "completed": true/false}

RULES:
1. ALWAYS use [TOOL:tool_name]{"args"} format
2. For delete/complete, use task name as task_id
3. After using tool, give brief confirmation

Example: User says "delete buy pen" → [TOOL:delete_task]{"task_id": "buy pen"}
Then say: "I've deleted the task 'buy pen'."
"""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history (limit to last 5 messages)
        if conversation_history:
            messages.extend(conversation_history[-5:])

        # Add current user message
        messages.append({"role": "user", "content": message})

        try:
            # Call OpenRouter API with retry logic for transient errors
            print(f'   → Calling OpenRouter API...')
            print(f'   Base URL: {self.base_url}, Model: {self.model}')

            # OpenRouter required headers
            timeout = 60.0
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Todo AI Chatbot",
            }

            # Retry logic for 500 errors (max 3 attempts)
            max_retries = 3
            retry_delay = 1.0

            response = None
            for attempt in range(max_retries):
                try:
                    response = httpx.post(
                        f"{self.base_url}/chat/completions",
                        json={
                            "model": self.model,
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 500,
                        },
                        headers=headers,
                        timeout=timeout
                    )

                    if response.status_code != 500:
                        break

                    if attempt < max_retries - 1:
                        print(f'   [WARN] Server error (500), retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})')
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        logger.warning(f"Max retries reached, last status: {response.status_code}")

                except httpx.RequestError as e:
                    if attempt < max_retries - 1:
                        print(f'   [WARN] Network error, retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})')
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        raise

            if response:
                response.raise_for_status()
            else:
                raise httpx.RequestError("No response from API")

            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f'   ← Response: "{content[:100]}..."')

            # Check for tool call
            tool_call = self._extract_tool_call(content)
            tool_calls = [tool_call] if tool_call else []

            if tool_call:
                print(f'   Tool call detected: {tool_call["name"]}')
                print(f'   Arguments: {tool_call["arguments"]}')
                result = self._execute_tool(tool_call["name"], tool_call["arguments"])
                print(f'   Tool result: {result.get("success", False)} - {result.get("message", "")}')

                # Clean the response
                clean_response = re.sub(r'\[TOOL:\w+\]\{[^}]+\}', '', content).strip()
                if not clean_response:
                    clean_response = "Task completed successfully!"
                content = clean_response
            else:
                print(f'   No tool call detected in response')

            return AgentResponse(content=content, tool_calls=tool_calls)

        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API HTTP error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")

                if e.response.status_code == 500:
                    return AgentResponse(
                        content="Sorry, the AI service is temporarily unavailable. Please try again.",
                        tool_calls=[]
                    )
                elif e.response.status_code == 401:
                    return AgentResponse(
                        content="API authentication failed. Please check your API key.",
                        tool_calls=[]
                    )
            return AgentResponse(
                content=f"Sorry, I encountered an API error: {str(e)}",
                tool_calls=[]
            )
        except httpx.HTTPError as e:
            logger.error(f"OpenRouter API error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return AgentResponse(
                content=f"Sorry, I encountered an API error: {str(e)}",
                tool_calls=[]
            )
        except Exception as e:
            logger.error(f"Agent processing failed: {type(e).__name__}: {str(e)}")
            return AgentResponse(
                content=f"Sorry, I encountered an error. Please try again.",
                tool_calls=[]
            )


def run_openrouter_agent(
    user_id: str,
    message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> AgentResponse:
    """Convenience function to process a message with OpenRouter agent."""
    agent = OpenRouterTodoAgent(user_id=user_id)
    return agent.process_message(message, conversation_history)
