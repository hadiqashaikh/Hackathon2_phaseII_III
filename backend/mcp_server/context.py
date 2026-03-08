"""
MCP Context for Phase III: Todo AI Chatbot.

This module provides context management for MCP tools, including user_id injection
from the authentication middleware.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPContext:
    """
    Context object passed to MCP tools.
    
    Contains user authentication information and other metadata
    that tools need to execute securely.
    """
    user_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from metadata."""
        return self.metadata.get(key, default)


def create_mcp_context(user_id: str, **kwargs) -> MCPContext:
    """
    Create an MCP context with user_id and optional metadata.
    
    Args:
        user_id: The authenticated user's ID
        **kwargs: Additional metadata to store in context
        
    Returns:
        MCPContext instance
    """
    return MCPContext(user_id=user_id, metadata=kwargs)
