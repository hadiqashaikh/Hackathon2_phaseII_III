"""
OpenAI Agent for Todo AI Chatbot - Phase III.

This module defines the OpenAI Agent with MCP tool bindings for task management.
Supports both OpenAI and OpenRouter API endpoints.

Updated for latest openai-agents SDK syntax with explicit tool binding.
"""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from agents import Agent, Runner, function_tool, ModelSettings
from agents.items import ModelResponse

from mcp_server.tools.task_tools import (
    add_task as mcp_add_task,
    list_tasks as mcp_list_tasks,
    complete_task as mcp_complete_task,
    delete_task as mcp_delete_task,
    update_task as mcp_update_task,
)
from mcp_server.context import create_mcp_context
from ai_agents.instructions import SYSTEM_INSTRUCTIONS, AGENT_NAME, AGENT_MODEL
from config import settings
from database import get_session_direct, engine
from sqlmodel import Session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ===========================================
# MCP Tool Wrappers for OpenAI Agents
# ===========================================

@function_tool
def add_task_tool(title: str) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        title: The task title (required, 1-255 characters)

    Returns:
        Dictionary with task details and confirmation message
    """
    print(f'\n[TOOL CALL] AI is calling tool: add_task_tool')
    print(f'   Parameters: title="{title}"')
    
    try:
        ctx = get_current_context()
        print(f'   User ID from context: {ctx.user_id}')

        # Create FRESH database session for this tool call
        fresh_session = Session(engine)
        try:
            # Temporarily patch the context to use fresh session
            import mcp_server.tools.task_tools as task_tools_module
            original_get_session = task_tools_module.get_session

            def fresh_session_generator():
                yield fresh_session
            task_tools_module.get_session = fresh_session_generator

            try:
                print(f'   Executing mcp_add_task...')
                result = mcp_add_task(ctx, title=title)
                print(f'   [SUCCESS] mcp_add_task returned: {result.get("success", False)}')
            except Exception as inner_error:
                print(f'   [FAILED] mcp_add_task FAILED: {type(inner_error).__name__}: {str(inner_error)}')
                raise
            finally:
                # Restore original function
                task_tools_module.get_session = original_get_session
        finally:
            fresh_session.close()
            print(f'   Database session closed')

        print(f'   Tool result: {result.get("message", "Success")}')
        print(f'   Task ID: {result.get("task", {}).get("id", "N/A")}\n')
        return result
    except Exception as e:
        print(f'   [ERROR] ERROR in add_task_tool: {type(e).__name__}: {str(e)}\n')
        logger.error(f"add_task_tool failed: {e}")
        logger.exception("Full traceback:")
        # Re-raise so the agent knows the tool failed
        raise


@function_tool
def list_tasks_tool(status: str = "all") -> Dict[str, Any]:
    """
    List all tasks for the authenticated user with optional status filter.

    Args:
        status: Filter tasks by status: 'all', 'pending', or 'completed'

    Returns:
        Dictionary with list of tasks and count
    """
    print(f'\n[TOOL CALL] AI is calling tool: list_tasks_tool')
    print(f'   Parameters: status="{status}"')
    
    try:
        ctx = get_current_context()

        # Create FRESH database session
        fresh_session = Session(engine)
        try:
            import mcp_server.tools.task_tools as task_tools_module
            original_get_session = task_tools_module.get_session

            def fresh_session_generator():
                yield fresh_session
            task_tools_module.get_session = fresh_session_generator

            try:
                print(f'   Executing mcp_list_tasks...')
                result = mcp_list_tasks(ctx, status=status)
            finally:
                task_tools_module.get_session = original_get_session
        finally:
            fresh_session.close()
            print(f'   Database session closed')

        print(f'   Found {result.get("count", 0)} tasks\n')
        return result
    except Exception as e:
        print(f'   [ERROR] ERROR in list_tasks_tool: {type(e).__name__}: {str(e)}\n')
        logger.error(f"list_tasks_tool failed: {e}")
        raise


@function_tool
def complete_task_tool(task_id: str) -> Dict[str, Any]:
    """
    Mark a specific task as completed for the authenticated user.

    Args:
        task_id: The ID of the task to complete

    Returns:
        Dictionary with updated task details and confirmation message
    """
    print(f'\n[TOOL CALL] AI is calling tool: complete_task_tool')
    print(f'   Parameters: task_id="{task_id}"')
    
    try:
        ctx = get_current_context()

        # Create FRESH database session
        fresh_session = Session(engine)
        try:
            import mcp_server.tools.task_tools as task_tools_module
            original_get_session = task_tools_module.get_session

            def fresh_session_generator():
                yield fresh_session
            task_tools_module.get_session = fresh_session_generator

            try:
                print(f'   Executing mcp_complete_task...')
                result = mcp_complete_task(ctx, task_id=task_id)
            finally:
                task_tools_module.get_session = original_get_session
        finally:
            fresh_session.close()
            print(f'   Database session closed')

        print(f'   Tool result: {result.get("message", "Success")}\n')
        return result
    except Exception as e:
        print(f'   [ERROR] ERROR in complete_task_tool: {type(e).__name__}: {str(e)}\n')
        logger.error(f"complete_task_tool failed: {e}")
        raise


@function_tool
def delete_task_tool(task_id: str) -> Dict[str, Any]:
    """
    Remove a specific task from the authenticated user's list.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Dictionary with success confirmation
    """
    print(f'\n[TOOL CALL] AI is calling tool: delete_task_tool')
    print(f'   Parameters: task_id="{task_id}"')
    
    try:
        ctx = get_current_context()

        # Create FRESH database session
        fresh_session = Session(engine)
        try:
            import mcp_server.tools.task_tools as task_tools_module
            original_get_session = task_tools_module.get_session

            def fresh_session_generator():
                yield fresh_session
            task_tools_module.get_session = fresh_session_generator

            try:
                print(f'   Executing mcp_delete_task...')
                result = mcp_delete_task(ctx, task_id=task_id)
            finally:
                task_tools_module.get_session = original_get_session
        finally:
            fresh_session.close()
            print(f'   Database session closed')

        print(f'   Tool result: {result.get("message", "Success")}\n')
        return result
    except Exception as e:
        print(f'   [ERROR] ERROR in delete_task_tool: {type(e).__name__}: {str(e)}\n')
        logger.error(f"delete_task_tool failed: {e}")
        raise


@function_tool
def update_task_tool(
    task_id: str,
    title: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Modify properties of an existing task for the authenticated user.

    Args:
        task_id: The ID of the task to update
        title: Optional new title
        completed: Optional completion status (True/False)

    Returns:
        Dictionary with updated task details and confirmation message
    """
    print(f'\n[TOOL CALL] AI is calling tool: update_task_tool')
    print(f'   Parameters: task_id="{task_id}", title={title}, completed={completed}')
    
    try:
        ctx = get_current_context()

        # Create FRESH database session
        fresh_session = Session(engine)
        try:
            import mcp_server.tools.task_tools as task_tools_module
            original_get_session = task_tools_module.get_session

            def fresh_session_generator():
                yield fresh_session
            task_tools_module.get_session = fresh_session_generator

            try:
                print(f'   Executing mcp_update_task...')
                result = mcp_update_task(ctx, task_id=task_id, title=title, completed=completed)
            finally:
                task_tools_module.get_session = original_get_session
        finally:
            fresh_session.close()
            print(f'   Database session closed')

        print(f'   Tool result: {result.get("message", "Success")}\n')
        return result
    except Exception as e:
        print(f'   [ERROR] ERROR in update_task_tool: {type(e).__name__}: {str(e)}\n')
        logger.error(f"update_task_tool failed: {e}")
        raise


# ===========================================
# Context Management
# ===========================================

import threading
_context_local = threading.local()

# Global context fallback for async tool execution
_global_context = None


def set_current_context(user_id: str):
    """Set the current MCP context for this thread."""
    global _global_context
    _context_local.context = create_mcp_context(user_id=user_id)
    _global_context = _context_local.context  # Also store globally as fallback


def get_current_context():
    """Get the current MCP context for this thread."""
    # Try thread-local first
    if hasattr(_context_local, 'context') and _context_local.context:
        return _context_local.context
    # Fallback to global context (for async tool execution)
    if _global_context:
        return _global_context
    # Last resort - raise error
    raise RuntimeError("No context set. Call set_current_context() first.")


def clear_context():
    """Clear the current context after request is complete."""
    global _global_context
    if hasattr(_context_local, 'context'):
        del _context_local.context
    _global_context = None


# ===========================================
# Agent Definition
# ===========================================

def create_todo_agent() -> Agent:
    """
    Create and configure the Todo AI Agent with OpenRouter/OpenAI support.

    Uses the latest openai-agents SDK syntax with explicit tool binding.
    """
    # Check if using OpenRouter
    is_openrouter = "openrouter.ai" in settings.OPENAI_BASE_URL

    logger.info(f"Creating Todo AI Agent: {AGENT_NAME}")
    logger.info(f"  Model: {AGENT_MODEL}")
    logger.info(f"  Base URL: {settings.OPENAI_BASE_URL}")
    logger.info(f"  Provider: {'OpenRouter' if is_openrouter else 'OpenAI'}")

    # Create OpenAI client with proper configuration
    from openai import OpenAI

    if is_openrouter:
        # OpenRouter configuration with required headers
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            default_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Todo AI Chatbot",
            }
        )
        logger.info("✓ OpenRouter client configured")
    else:
        # Standard OpenAI configuration
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
        )
        logger.info("✓ OpenAI client configured")

    # Define all tools explicitly
    all_tools = [
        add_task_tool,
        list_tasks_tool,
        complete_task_tool,
        delete_task_tool,
        update_task_tool,
    ]

    # Create agent with explicit tool binding
    agent = Agent(
        name=AGENT_NAME,
        instructions=SYSTEM_INSTRUCTIONS,
        model=AGENT_MODEL,
        model_settings=ModelSettings(
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=0.7,
        ),
        # Explicitly pass tools list to agent
        tools=all_tools,
    )

    # Store the client on the agent for use during execution
    agent._client = client

    # Print tool registration summary
    print('\n' + '='*60)
    print('TODO AI AGENT INITIALIZED')
    print('='*60)
    print(f'  Name: {AGENT_NAME}')
    print(f'  Model: {AGENT_MODEL}')
    print(f'  Provider: {"OpenRouter" if is_openrouter else "OpenAI"}')
    print(f'  Max Tokens: {settings.OPENAI_MAX_TOKENS}')
    print(f'  Tools Registered (explicit binding):')
    for tool in all_tools:
        print(f'    [CHECK] {tool.name if hasattr(tool, "name") else tool.__name__}')
    print('='*60 + '\n')

    logger.info(f"✓ Created Todo AI Agent: {AGENT_NAME}")
    return agent


# Global agent instance (lazy-loaded)
_agent_instance: Optional[Agent] = None


def get_agent() -> Agent:
    """Get or create the global agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_todo_agent()
    return _agent_instance


# ===========================================
# Agent Runner (Stateless)
# ===========================================

@dataclass
class AgentResponse:
    """Response from agent processing."""
    content: str
    tool_calls: List[Dict[str, Any]]
    conversation_id: Optional[str] = None


class TodoAgentRunner:
    """
    Stateless runner for the Todo AI Agent.

    This class handles message processing, maintaining conversation context
    through the caller rather than storing state internally.
    """

    def __init__(self, user_id: str):
        """
        Initialize the runner with user context.

        Args:
            user_id: The authenticated user's ID
        """
        self.user_id = user_id
        self._context = None  # Store context directly on instance
        try:
            self._agent = get_agent()
            logger.info(f"Agent initialized for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise

    async def process_message(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> AgentResponse:
        """
        Process a user message and generate an AI response.

        Args:
            message: The user's message
            conversation_history: Optional list of previous messages
                Format: [{"role": "user"|"assistant", "content": "..."}]

        Returns:
            AgentResponse with content and any tool calls made
        """
        try:
            # Set context for this request - store on both thread-local AND instance
            set_current_context(self.user_id)
            self._context = create_mcp_context(user_id=self.user_id)
            print(f'\n[AGENT] Processing message for user_id: {self.user_id}')
            print(f'   Message: "{message[:100]}..."')
            print(f'   Context created: user_id={self._context.user_id}')

            # Build input messages
            input_messages = []

            # Add conversation history if provided
            if conversation_history:
                input_messages.extend(conversation_history)

            # Add current user message
            input_messages.append({"role": "user", "content": message})

            logger.info(f"Processing message for user_id: {self.user_id}")
            logger.debug(f"Input messages: {len(input_messages)}")

            # Run the agent - tools are already bound to the agent
            print(f'   Running agent...')
            result = await Runner.run(
                self._agent,
                input=input_messages,
            )

            # Extract response content
            content = result.final_output
            print(f'   Agent response: "{content[:100]}..."')

            # Extract tool calls from the result
            tool_calls = []
            if hasattr(result, 'tool_calls') and result.tool_calls:
                print(f'   Tool calls detected: {len(result.tool_calls)}')
                for tc in result.tool_calls:
                    tool_call_data = {
                        "name": tc.name if hasattr(tc, 'name') else str(tc),
                        "arguments": tc.arguments if hasattr(tc, 'arguments') else {},
                    }
                    tool_calls.append(tool_call_data)
                    print(f'     - {tool_call_data["name"]}: {tool_call_data["arguments"]}')
            else:
                print(f'   No tool calls in result')

            logger.info(f"Agent response generated. Tool calls: {len(tool_calls)}")

            return AgentResponse(
                content=content,
                tool_calls=tool_calls,
            )

        except Exception as e:
            logger.error(f"Agent processing failed: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            raise
        finally:
            # Clear context after request is complete
            clear_context()
            print(f'   Context cleared\n')

    def process_message_sync(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> AgentResponse:
        """
        Synchronous version of process_message.

        Args:
            message: The user's message
            conversation_history: Optional list of previous messages

        Returns:
            AgentResponse with content and any tool calls made
        """
        import asyncio

        try:
            # Check if we're already in an event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # We're in a running loop, need to run in a new thread
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(
                            asyncio.run,
                            self.process_message(message, conversation_history)
                        )
                        return future.result()
            except RuntimeError:
                pass  # No event loop, proceed normally

            return asyncio.run(self.process_message(message, conversation_history))

        except Exception as e:
            logger.error(f"Sync agent processing failed: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            raise


# ===========================================
# Convenience Functions
# ===========================================

def run_agent_message(
    user_id: str,
    message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> AgentResponse:
    """
    Convenience function to process a single message.

    Args:
        user_id: The authenticated user's ID
        message: The user's message
        conversation_history: Optional list of previous messages

    Returns:
        AgentResponse with content and any tool calls
    """
    try:
        runner = TodoAgentRunner(user_id=user_id)
        return runner.process_message_sync(message, conversation_history)
    except Exception as e:
        logger.error(f"Convenience function failed: {type(e).__name__}: {str(e)}")
        raise
