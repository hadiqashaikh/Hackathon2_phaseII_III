"""
MCP Context for tool execution.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MCPContext:
    """Context for MCP tools."""
    user_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def create_mcp_context(user_id: str, **kwargs) -> MCPContext:
    """Create MCP context with user_id."""
    return MCPContext(user_id=user_id, metadata=kwargs)
