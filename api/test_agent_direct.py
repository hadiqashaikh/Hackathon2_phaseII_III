"""
Test the agent and task tools directly.
"""

import sys
sys.path.insert(0, '.')

from mcp_server.context import create_mcp_context
from mcp_server.tools.task_tools import add_task, list_tasks

# Test adding a task
print("=" * 50)
print("Testing Task Creation")
print("=" * 50)

ctx = create_mcp_context(user_id="test-user")

try:
    print("\n1. Adding task: 'buy clothes'")
    result = add_task(ctx, title="buy clothes")
    print(f"Result: {result}")
    
    print("\n2. Listing all tasks")
    result = list_tasks(ctx, status="all")
    print(f"Result: {result}")
    
    print("\n✅ Tests passed!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
