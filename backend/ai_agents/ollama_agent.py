"""
Simple Ollama Agent for Todo AI Chatbot.

This module provides a lightweight agent that works with Ollama's chat completions API.
No external dependencies - uses httpx which is already installed.
"""

import logging
import json
import re
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
from ai_agents.instructions import SYSTEM_INSTRUCTIONS
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


class OllamaTodoAgent:
    """
    Simple Ollama-based agent for todo management.
    """

    def __init__(self, user_id: str):
        """
        Initialize the agent with user context.

        Args:
            user_id: The authenticated user's ID
        """
        self.user_id = user_id
        self._context = None
        self.base_url = settings.OPENAI_BASE_URL.replace("/v1", "")
        self.model = settings.OPENAI_AGENT_MODEL
        # Keep model loaded in memory for faster responses
        self._keep_alive = "5m"
        logger.info(f"OllamaTodoAgent initialized for user: {user_id}")
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
                    completed=arguments.get("completed")
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
        # Pattern: [TOOL:tool_name]{"arg": "value"}
        pattern = r'\[TOOL:(\w+)\](\{[^}]+\})'
        match = re.search(pattern, text)
        
        if match:
            try:
                tool_name = match.group(1)
                args = json.loads(match.group(2))
                return {"name": tool_name, "arguments": args}
            except:
                pass
        return None

    def process_message(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> AgentResponse:
        """Process a user message and generate an AI response."""
        print(f'\n🤖 [OLLAMA AGENT] Processing message for user: {self.user_id}')
        print(f'   Message: "{message[:100]}..."')

        # Build system prompt with tool instructions
        system_prompt = """You are a helpful todo assistant. You can manage tasks using these tools:

[TOOL:add_task]{"title": "task name"} - Create a new task
[TOOL:list_tasks]{"status": "all|pending|completed"} - List tasks
[TOOL:complete_task]{"task_id": "task name or id"} - Mark task complete (use task name directly)
[TOOL:delete_task]{"task_id": "task name or id"} - Delete a task (use task name directly)
[TOOL:update_task]{"task_id": "task name or id", "title": "new title", "completed": true/false} - Update task

IMPORTANT: For delete/complete/update, you can use the task NAME directly as task_id. 
Example: User says "delete the task to buy sugar" → [TOOL:delete_task]{"task_id": "buy sugar"}

When you need to use a tool, respond with: [TOOL:tool_name]{"arg": "value"}
Then provide a natural response to the user.

Be concise and helpful."""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-10:])

        # Add current user message
        messages.append({"role": "user", "content": message})

        try:
            # Call Ollama API
            print(f'   → Calling Ollama API...')
            print(f'   Base URL: {self.base_url}, Model: {self.model}')
            
            # Increase timeout for first request (model loading can take time)
            timeout = 120.0  # First request needs more time to load model
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300,  # Limit response tokens for speed
                        "top_p": 0.9
                    },
                    "keep_alive": "10m"  # Keep model loaded for 10 min for faster subsequent calls
                },
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()

            content = result.get("message", {}).get("content", "")
            print(f'   ← Response: "{content[:100]}..."')

            # Check for tool call
            tool_call = self._extract_tool_call(content)
            tool_calls = [tool_call] if tool_call else []

            if tool_call:
                print(f'   Tool call detected: {tool_call["name"]}')
                # Execute the tool
                self._execute_tool(tool_call["name"], tool_call["arguments"])

                # Clean the response (remove tool call syntax)
                clean_response = re.sub(r'\[TOOL:\w+\]\{[^}]+\}', '', content).strip()
                if not clean_response:
                    clean_response = "Task completed successfully!"
                content = clean_response

            return AgentResponse(content=content, tool_calls=tool_calls)

        except httpx.HTTPError as e:
            logger.error(f"Ollama API error: {e}")
            return AgentResponse(
                content=f"Sorry, I encountered an error: {str(e)}",
                tool_calls=[]
            )
        except Exception as e:
            logger.error(f"Agent processing failed: {type(e).__name__}: {str(e)}")
            return AgentResponse(
                content=f"Sorry, I encountered an error. Please try again.",
                tool_calls=[]
            )


# Convenience function
def run_ollama_agent(
    user_id: str,
    message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> AgentResponse:
    """Convenience function to process a message with Ollama agent."""
    agent = OllamaTodoAgent(user_id=user_id)
    return agent.process_message(message, conversation_history)
