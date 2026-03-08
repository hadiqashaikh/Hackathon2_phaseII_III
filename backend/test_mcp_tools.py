"""
Test Script for MCP Tools - Phase III: Todo AI Chatbot.

This script tests all 5 MCP tools with a mock user_id to verify they work correctly.
Run this script to validate the MCP tools implementation.

Usage:
    python test_mcp_tools.py
"""

import uuid
from mcp_server.context import create_mcp_context
from mcp_server.tools.task_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)

# Mock user_id for testing (use a real user from your database)
# Run: python get_user_id.py to get a valid user ID
TEST_USER_ID = "JYiKapNmtoTvWj3TGdRnZpQeVDTgp7xP"


def test_add_task():
    """Test adding a new task."""
    print("\n" + "=" * 60)
    print("TEST: add_task")
    print("=" * 60)
    
    ctx = create_mcp_context(user_id=TEST_USER_ID)
    
    try:
        result = add_task(ctx, title="Buy groceries")
        print(f"[SUCCESS] {result['message']}")
        print(f"Task ID: {result['task']['id']}")
        return result['task']['id']
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_list_tasks():
    """Test listing tasks."""
    print("\n" + "=" * 60)
    print("TEST: list_tasks")
    print("=" * 60)
    
    ctx = create_mcp_context(user_id=TEST_USER_ID)
    
    try:
        result = list_tasks(ctx, status="all")
        print(f"[SUCCESS] {result['message']}")
        print(f"Tasks found: {result['count']}")
        for task in result['tasks'][:3]:  # Show first 3 tasks
            status_icon = "[x]" if task['completed'] else "[ ]"
            print(f"  {status_icon} {task['title']}")
        return result
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_complete_task(task_id):
    """Test completing a task."""
    print("\n" + "=" * 60)
    print("TEST: complete_task")
    print("=" * 60)
    
    ctx = create_mcp_context(user_id=TEST_USER_ID)
    
    try:
        result = complete_task(ctx, task_id=task_id)
        print(f"[SUCCESS] {result['message']}")
        return result
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_update_task(task_id):
    """Test updating a task."""
    print("\n" + "=" * 60)
    print("TEST: update_task")
    print("=" * 60)
    
    ctx = create_mcp_context(user_id=TEST_USER_ID)
    
    try:
        result = update_task(
            ctx,
            task_id=task_id,
            completed=True
        )
        print(f"[SUCCESS] {result['message']}")
        print(f"Updates: {', '.join(result['updates'])}")
        return result
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_delete_task(task_id):
    """Test deleting a task."""
    print("\n" + "=" * 60)
    print("TEST: delete_task")
    print("=" * 60)
    
    ctx = create_mcp_context(user_id=TEST_USER_ID)
    
    try:
        result = delete_task(ctx, task_id=task_id)
        print(f"[SUCCESS] {result['message']}")
        return result
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_unauthorized_access():
    """Test that tools reject missing user_id."""
    print("\n" + "=" * 60)
    print("TEST: Unauthorized Access (should fail)")
    print("=" * 60)
    
    # Create context without user_id
    ctx = create_mcp_context(user_id="")
    
    try:
        result = list_tasks(ctx)
        print(f"[ERROR] Should have raised an exception but got: {result}")
        return False
    except Exception as e:
        print(f"[SUCCESS] Correctly rejected unauthorized access: {str(e)}")
        return True


def main():
    """Run all MCP tool tests."""
    print("\n" + "=" * 60)
    print("Phase III: MCP Tools Test Suite")
    print("=" * 60)
    print(f"Test User ID: {TEST_USER_ID}")
    
    # Test 1: Add a task
    task_id = test_add_task()
    
    if not task_id:
        print("\n[ABORT] Cannot continue tests without a task ID")
        return
    
    # Test 2: List tasks
    test_list_tasks()
    
    # Test 3: Complete the task
    test_complete_task(task_id)
    
    # Test 4: Update the task
    test_update_task(task_id)
    
    # Test 5: Delete the task
    test_delete_task(task_id)
    
    # Test 6: Unauthorized access
    test_unauthorized_access()
    
    print("\n" + "=" * 60)
    print("All MCP Tool Tests Completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
