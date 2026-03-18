"""
OpenRouter Agent for Todo Management.
Fixed: API 401 errors, better logging, proper headers.
"""

import logging
import re
import json
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

import httpx

from mcp_server.tools.task_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)
from mcp_server.context import create_mcp_context
from config import settings

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Agent response."""
    content: str
    tool_calls: List[Dict[str, Any]]
    conversation_id: Optional[str] = None


def format_tool_call(name: str, arguments: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    """Format tool call for frontend consumption."""
    tool_name = name.replace('_task', '_task_tool')  # Match frontend expectation
    return {
        "tool": tool_name,
        "result": result,
        "arguments": arguments,
    }


class OpenRouterAgent:
    """OpenRouter-based agent."""

    def __init__(self, user_id: str):
        self.user_id = user_id.strip() if user_id else ""
        self.base_url = settings.OPENROUTER_BASE_URL.strip()
        self.api_key = settings.OPENROUTER_API_KEY.strip() if settings.OPENROUTER_API_KEY else ""
        self.model = settings.OPENROUTER_AGENT_MODEL.strip() if settings.OPENROUTER_AGENT_MODEL else ""
        
        logger.info(f"OpenRouterAgent initialized for user: {self.user_id}")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Model: {self.model}")
        logger.info(f"API Key present: {bool(self.api_key)}")
        logger.info(f"API Key prefix: {self.api_key[:15]}..." if self.api_key else "NO API KEY")

    def _execute_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with proper error handling."""
        ctx = create_mcp_context(user_id=self.user_id)
        logger.info(f"Executing tool: {name} with args: {args}")
        logger.info(f"MCP Context user_id: '{ctx.user_id}'")

        try:
            if name == "add_task":
                title = args.get("title", "").strip()
                if not title:
                    return {"success": False, "error": "Task title is required"}
                logger.info(f"Calling add_task with title: '{title}'")
                result = add_task(ctx, title=title)
                logger.info(f"add_task result: {result}")
                return result
            elif name == "list_tasks":
                result = list_tasks(ctx, status=args.get("status", "all"))
                return result
            elif name == "complete_task":
                result = complete_task(ctx, task_id=args.get("task_id", ""))
                return result
            elif name == "delete_task":
                result = delete_task(ctx, task_id=args.get("task_id", ""))
                return result
            elif name == "update_task":
                result = update_task(
                    ctx,
                    task_id=args.get("task_id", ""),
                    title=args.get("title"),
                    completed=args.get("completed"),
                )
                return result
            else:
                return {"success": False, "error": f"Unknown tool: {name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {type(e).__name__}: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _format_tool_call_for_response(self, name: str, arguments: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Format tool call for frontend - matches expected structure."""
        tool_name = name.replace('_task', '_task_tool')  # Match frontend: add_task_tool
        return {
            "tool": tool_name,
            "result": result,
            "arguments": arguments,
        }

    def _extract_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract tool call from text with multiple patterns."""
        logger.debug(f"Extracting tool call from: {text[:200]}")

        # Pattern 1: [TOOL:name]{"args"}
        pattern = r'\[TOOL:(\w+)\](\{[^}]+\})'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            try:
                name = match.group(1)
                args_str = match.group(2)
                logger.info(f"Found tool pattern: {name} with {args_str}")
                args = json.loads(args_str)
                return {"name": name, "arguments": args}
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON: {args_str}, error: {e}")

        # Pattern 2: Natural language detection for common commands
        text_lower = text.lower()

        # Add task detection
        if any(word in text_lower for word in ['add task', 'create task', 'add a task']):
            # Extract task title from quotes or after "add task"
            title_match = re.search(r'["\']([^"\']+)["\']', text)
            if not title_match:
                # Try to extract after "add task"
                add_match = re.search(r'add(?:\s+a)?\s+task[:\s]+(.+?)(?:\.|$)', text_lower)
                if add_match:
                    title = add_match.group(1).strip()
                    return {"name": "add_task", "arguments": {"title": title}}
            elif title_match:
                return {"name": "add_task", "arguments": {"title": title_match.group(1)}}

        return None

    def process_message(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> AgentResponse:
        """Process user message with improved error handling and detailed logging."""
        logger.info(f"Processing message: {message}")
        logger.info(f"User ID: '{self.user_id}'")

        # If no API key, return a helpful message
        if not self.api_key or self.api_key == "sk-or-v1-your-api-key-here":
            logger.error("NO API KEY CONFIGURED!")
            return AgentResponse(
                content="AI is not configured. Please add your OPENROUTER_API_KEY to the .env file.",
                tool_calls=[]
            )

        system_prompt = """You are a helpful todo assistant.

CRITICAL: Use tools with this EXACT format (no spaces after TOOL:):
[TOOL:add_task]{"title": "task name"}
[TOOL:list_tasks]{"status": "all"}
[TOOL:complete_task]{"task_id": "task name"}
[TOOL:delete_task]{"task_id": "task name"}
[TOOL:update_task]{"task_id": "task name", "title": "new title"}

Rules:
1. ALWAYS use the exact format above
2. For task_id, use the exact task title
3. After using a tool, confirm what you did
4. Be brief and friendly

Examples:
User: "add task buy milk"
You: [TOOL:add_task]{"title": "buy milk"}
I've added the task: buy milk

User: "what are my tasks?"
You: [TOOL:list_tasks]{"status": "all"}
You have 2 tasks: [list them]
"""

        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history[-5:])
        messages.append({"role": "user", "content": message})

        # Build the request
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Todo AI Chatbot",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500,
        }

        logger.info("=" * 60)
        logger.info(f"OPENROUTER REQUEST")
        logger.info(f"URL: {url}")
        logger.info(f"Headers: Authorization=Bearer {self.api_key[:10]}..., Content-Type=application/json")
        logger.info(f"Model: {self.model}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        logger.info("=" * 60)

        try:
            response = httpx.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )

            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Body: {response.text}")

            # Handle 401 Unauthorized specifically
            if response.status_code == 401:
                logger.error("❌ OPENROUTER 401 UNAUTHORIZED!")
                logger.error(f"API Key used: {self.api_key[:15]}...")
                logger.error(f"Full response: {response.text}")
                return AgentResponse(
                    content=f"API Error (401): Invalid API key. Please check your OpenRouter API key in .env file. Key starts with: {self.api_key[:20]}...",
                    tool_calls=[]
                )

            # Handle other errors
            if response.status_code >= 400:
                logger.error(f"❌ OPENROUTER ERROR {response.status_code}!")
                logger.error(f"Response: {response.text}")
                return AgentResponse(
                    content=f"API Error ({response.status_code}): {response.text[:200]}",
                    tool_calls=[]
                )

            response.raise_for_status()

            result = response.json()
            logger.info(f"Parsed result: {json.dumps(result, indent=2)[:500]}")

            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            logger.info(f"AI content: {content}")

            # Check for tool call
            tool_call = self._extract_tool_call(content)
            
            # Format tool_calls for frontend
            tool_calls = []
            if tool_call:
                logger.info(f"Tool call detected: {tool_call['name']}")
                tool_result = self._execute_tool(tool_call["name"], tool_call["arguments"])

                if tool_result.get("success"):
                    logger.info(f"Tool executed successfully")
                    # Format tool call for frontend
                    formatted_tool_call = self._format_tool_call_for_response(
                        tool_call["name"],
                        tool_call["arguments"],
                        tool_result
                    )
                    tool_calls = [formatted_tool_call]
                    
                    # Clean response
                    content = re.sub(r'\[TOOL:\w+\]\{[^}]+\}', '', content, flags=re.IGNORECASE).strip()
                    if not content or len(content) < 10:
                        # Generate a friendly response based on tool result
                        if tool_call['name'] == 'add_task':
                            task_title = tool_call['arguments'].get('title', 'task')
                            content = f"I've added the task: {task_title}"
                        elif tool_call['name'] == 'list_tasks':
                            count = tool_result.get('count', 0)
                            content = f"You have {count} task(s)."
                        elif tool_call['name'] == 'complete_task':
                            content = "Task marked as complete! Great job!"
                        elif tool_call['name'] == 'delete_task':
                            content = "Task deleted successfully."
                else:
                    error_msg = tool_result.get('error', 'Unknown error')
                    content = f"Sorry, I couldn't complete that action: {error_msg}"
                    logger.error(f"Tool failed: {error_msg}")

            return AgentResponse(content=content, tool_calls=tool_calls)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e.response.status_code}")
            logger.error(f"Response: {e.response.text}")
            logger.exception("Full traceback:")
            return AgentResponse(
                content=f"API Error ({e.response.status_code}): {e.response.text[:200]}",
                tool_calls=[]
            )
        except httpx.RequestError as e:
            logger.error(f"Request Error: {str(e)}")
            logger.exception("Full traceback:")
            return AgentResponse(
                content=f"Network Error: Unable to connect to AI service. Please check your internet connection.",
                tool_calls=[]
            )
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            return AgentResponse(
                content=f"Sorry, I encountered an unexpected error: {str(e)}",
                tool_calls=[]
            )


def run_agent(user_id: str, message: str, history: Optional[List[Dict[str, str]]] = None) -> AgentResponse:
    """Convenience function to run agent."""
    agent = OpenRouterAgent(user_id=user_id)
    return agent.process_message(message, history)
