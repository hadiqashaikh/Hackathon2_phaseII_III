"""
OpenAI Agents package for Phase III: Todo AI Chatbot.
"""

from ai_agents.todo_agent import (
    create_todo_agent,
    get_agent,
    TodoAgentRunner,
    run_agent_message,
    AgentResponse,
)

from ai_agents.instructions import SYSTEM_INSTRUCTIONS, AGENT_NAME, AGENT_MODEL

__all__ = [
    "create_todo_agent",
    "get_agent",
    "TodoAgentRunner",
    "run_agent_message",
    "AgentResponse",
    "SYSTEM_INSTRUCTIONS",
    "AGENT_NAME",
    "AGENT_MODEL",
]
