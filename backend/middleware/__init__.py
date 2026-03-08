"""
Authentication middleware for Phase III: Todo AI Chatbot.

Exports authentication dependencies for use in routes and MCP tools.
"""

from middleware.auth import (
    get_current_user_id,
    get_current_user_payload,
    get_optional_user_id,
    verify_session_token,
    AuthError,
)

__all__ = [
    "get_current_user_id",
    "get_current_user_payload",
    "get_optional_user_id",
    "verify_session_token",
    "AuthError",
]
