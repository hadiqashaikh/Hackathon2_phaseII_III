"""
MCP Tools for Task Management - Phase III: Todo AI Chatbot.

This module implements 5 MCP tools for managing tasks:
- add_task: Create a new task
- list_tasks: List all tasks with optional filtering
- complete_task: Mark a task as completed
- delete_task: Remove a task
- update_task: Modify an existing task

All tools enforce user_id-based data isolation to ensure users can only
access their own tasks.
"""

import logging
import uuid
from typing import Optional, List, Dict, Any

from sqlmodel import Session, select
from mcp.server import FastMCP

from models import Task, TaskCreate, TaskUpdate
from database import get_session
from mcp_server.context import MCPContext

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP(name="todo-ai-mcp-server")


# ===========================================
# Helper Functions
# ===========================================

def get_db_session() -> Session:
    """Get a database session."""
    return next(get_session())


def format_task_response(task: Task) -> Dict[str, Any]:
    """Format a task for user-friendly response."""
    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
    }


# ===========================================
# MCP Tool: add_task
# ===========================================

@mcp.tool()
def add_task(
    ctx: MCPContext,
    title: str,
) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        ctx: MCP context containing user_id (auto-injected by auth middleware)
        title: The task title (required, 1-255 characters)

    Returns:
        Dictionary with task details and user-friendly message

    Raises:
        ValueError: If title is empty or too long
        HTTPException: If user_id is missing (401 Unauthorized)
    """
    # Validate user_id from context
    if not ctx.user_id:
        logger.error("add_task called without user_id")
        raise Exception("Unauthorized: User ID not found in context")

    # Validate title
    if not title or len(title.strip()) == 0:
        raise ValueError("Task title cannot be empty")

    if len(title) > 255:
        raise ValueError("Task title must be 255 characters or less")

    print(f'\n💾 [DATABASE] Saving to DB: "{title}"')
    print(f'   User ID: {ctx.user_id}')
    logger.info(f"Creating task for user_id: {ctx.user_id}, title: {title}")
    
    try:
        with get_db_session() as session:
            # Generate a unique task ID (TEXT format to match Phase II schema)
            task_id = str(uuid.uuid4())
            
            # Create new task with user_id from context
            task = Task(
                id=task_id,
                title=title.strip(),
                completed=False,
                user_id=ctx.user_id
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"Task created successfully with id: {task.id}")
            
            return {
                "success": True,
                "message": f'Task "{task.title}" has been created successfully',
                "task": format_task_response(task),
            }
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise Exception(f"Failed to create task: {str(e)}")


# ===========================================
# MCP Tool: list_tasks
# ===========================================

@mcp.tool()
def list_tasks(
    ctx: MCPContext,
    status: str = "all"
) -> Dict[str, Any]:
    """
    List all tasks for the authenticated user with optional status filter.
    
    Args:
        ctx: MCP context containing user_id (auto-injected by auth middleware)
        status: Filter tasks by status: 'all', 'pending', or 'completed'
    
    Returns:
        Dictionary with list of tasks and count
    
    Raises:
        ValueError: If status is not a valid option
        HTTPException: If user_id is missing (401 Unauthorized)
    """
    # Validate user_id from context
    if not ctx.user_id:
        logger.error("list_tasks called without user_id")
        raise Exception("Unauthorized: User ID not found in context")
    
    # Validate status filter
    valid_statuses = ["all", "pending", "completed"]
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}")
    
    logger.info(f"Listing tasks for user_id: {ctx.user_id}, status: {status}")
    
    try:
        with get_db_session() as session:
            # Build query with user_id filter (data isolation)
            query = select(Task).where(Task.user_id == ctx.user_id)
            
            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            
            # Order by created_at descending (newest first)
            query = query.order_by(Task.created_at.desc())
            
            tasks = session.exec(query).all()
            
            logger.info(f"Retrieved {len(tasks)} tasks for user_id: {ctx.user_id}")
            
            # Format response based on status
            if status == "pending":
                status_label = "pending"
            elif status == "completed":
                status_label = "completed"
            else:
                status_label = "all"
            
            return {
                "success": True,
                "message": f"Found {len(tasks)} {status_label} task(s)",
                "count": len(tasks),
                "status_filter": status,
                "tasks": [format_task_response(task) for task in tasks],
            }
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise Exception(f"Failed to list tasks: {str(e)}")


# ===========================================
# MCP Tool: complete_task
# ===========================================

@mcp.tool()
def complete_task(
    ctx: MCPContext,
    task_id: str
) -> Dict[str, Any]:
    """
    Mark a specific task as completed for the authenticated user.

    Args:
        ctx: MCP context containing user_id (auto-injected by auth middleware)
        task_id: The ID of the task to complete (as string). Can also be a task title/description.

    Returns:
        Dictionary with updated task details and user-friendly message

    Raises:
        ValueError: If task_id is invalid format
        NotFoundError: If task not found or doesn't belong to user
        HTTPException: If user_id is missing (401 Unauthorized)
    """
    # Validate user_id from context
    if not ctx.user_id:
        logger.error("complete_task called without user_id")
        raise Exception("Unauthorized: User ID not found in context")

    # Validate task_id (ensure it's a string for TEXT column comparison)
    task_id_str = str(task_id).strip()

    logger.info(f"Completing task '{task_id}' for user_id: {ctx.user_id}")

    try:
        with get_db_session() as session:
            # First, try to find by exact ID match
            task = session.exec(
                select(Task).where(
                    Task.id == task_id_str,
                    Task.user_id == ctx.user_id
                )
            ).first()

            # If not found by ID, try to find by title (case-insensitive partial match)
            if not task:
                logger.info(f"Task not found by ID '{task_id_str}', searching by title...")
                task = session.exec(
                    select(Task).where(
                        Task.user_id == ctx.user_id,
                        Task.title.ilike(f"%{task_id_str}%")
                    )
                ).first()
                
                if task:
                    logger.info(f"Found task by title match: '{task.title}' (ID: {task.id})")

            if not task:
                logger.warning(f"Task '{task_id}' not found or not owned by user {ctx.user_id}")
                raise Exception(f"Task not found. The task may not exist or you don't have permission to access it.")

            if task.completed:
                return {
                    "success": True,
                    "message": f'Task "{task.title}" was already completed',
                    "task": format_task_response(task),
                    "already_completed": True,
                }

            # Mark as completed
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task '{task_id}' marked as completed for user_id: {ctx.user_id}")

            return {
                "success": True,
                "message": f'Task "{task.title}" has been marked as complete! Great job!',
                "task": format_task_response(task),
            }
    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error completing task: {str(e)}")
        raise Exception(f"Failed to complete task: {str(e)}")


# ===========================================
# MCP Tool: delete_task
# ===========================================

@mcp.tool()
def delete_task(
    ctx: MCPContext,
    task_id: str
) -> Dict[str, Any]:
    """
    Remove a specific task from the authenticated user's list.

    Args:
        ctx: MCP context containing user_id (auto-injected by auth middleware)
        task_id: The ID of the task to delete (as string). Can also be a task title/description.

    Returns:
        Dictionary with success confirmation and deleted task info

    Raises:
        ValueError: If task_id is invalid format
        NotFoundError: If task not found or doesn't belong to user
        HTTPException: If user_id is missing (401 Unauthorized)
    """
    # Validate user_id from context
    if not ctx.user_id:
        logger.error("delete_task called without user_id")
        raise Exception("Unauthorized: User ID not found in context")

    # Validate task_id (ensure it's a string for TEXT column comparison)
    task_id_str = str(task_id).strip()

    logger.info(f"Deleting task '{task_id}' for user_id: {ctx.user_id}")

    try:
        with get_db_session() as session:
            # First, try to find by exact ID match
            task = session.exec(
                select(Task).where(
                    Task.id == task_id_str,
                    Task.user_id == ctx.user_id
                )
            ).first()

            # If not found by ID, try to find by title (case-insensitive partial match)
            # This handles cases where AI extracts task description instead of UUID
            if not task:
                logger.info(f"Task not found by ID '{task_id_str}', searching by title...")
                task = session.exec(
                    select(Task).where(
                        Task.user_id == ctx.user_id,
                        Task.title.ilike(f"%{task_id_str}%")
                    )
                ).first()
                
                if task:
                    logger.info(f"Found task by title match: '{task.title}' (ID: {task.id})")

            if not task:
                logger.warning(f"Task '{task_id}' not found or not owned by user {ctx.user_id}")
                raise Exception(f"Task not found. The task may not exist or you don't have permission to delete it.")

            task_title = task.title
            session.delete(task)
            session.commit()

            logger.info(f"Task '{task_id}' deleted successfully for user_id: {ctx.user_id}")

            return {
                "success": True,
                "message": f'Task "{task_title}" has been deleted successfully',
                "deleted_id": task.id,
            }
    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error deleting task: {str(e)}")
        raise Exception(f"Failed to delete task: {str(e)}")


# ===========================================
# MCP Tool: update_task
# ===========================================

@mcp.tool()
def update_task(
    ctx: MCPContext,
    task_id: str,
    title: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Modify properties of an existing task for the authenticated user.

    Args:
        ctx: MCP context containing user_id (auto-injected by auth middleware)
        task_id: The UUID of the task to update (as string). Can also be a task title/description.
        title: Optional new title (1-255 characters)
        completed: Optional completion status (True/False)

    Returns:
        Dictionary with updated task details and user-friendly message

    Raises:
        ValueError: If title is empty or too long
        NotFoundError: If task not found or doesn't belong to user
        HTTPException: If user_id is missing (401 Unauthorized)
    """
    # Validate user_id from context
    if not ctx.user_id:
        logger.error("update_task called without user_id")
        raise Exception("Unauthorized: User ID not found in context")

    # Validate title if provided
    if title is not None:
        if len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        if len(title) > 255:
            raise ValueError("Task title must be 255 characters or less")

    # Check if at least one field is being updated
    if title is None and completed is None:
        raise ValueError("At least one field (title or completed) must be provided for update")

    logger.info(f"Updating task '{task_id}' for user_id: {ctx.user_id}")

    try:
        with get_db_session() as session:
            # First, try to find by exact ID match
            task = session.exec(
                select(Task).where(
                    Task.id == str(task_id),
                    Task.user_id == ctx.user_id
                )
            ).first()

            # If not found by ID, try to find by title (case-insensitive partial match)
            if not task:
                logger.info(f"Task not found by ID '{task_id}', searching by title...")
                task = session.exec(
                    select(Task).where(
                        Task.user_id == ctx.user_id,
                        Task.title.ilike(f"%{task_id}%")
                    )
                ).first()
                
                if task:
                    logger.info(f"Found task by title match: '{task.title}' (ID: {task.id})")

            if not task:
                logger.warning(f"Task '{task_id}' not found or not owned by user {ctx.user_id}")
                raise Exception(f"Task not found. The task may not exist or you don't have permission to update it.")

            # Track what's being updated
            updates = []

            # Update fields if provided
            if title is not None:
                old_title = task.title
                task.title = title.strip()
                updates.append(f"title: '{old_title}' to '{task.title}'")

            if completed is not None:
                old_completed = task.completed
                task.completed = completed
                updates.append(f"completed: {old_completed} to {completed}")

            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Task '{task_id}' updated for user_id: {ctx.user_id}. Changes: {', '.join(updates)}")

            return {
                "success": True,
                "message": f'Task "{task.title}" has been updated successfully',
                "task": format_task_response(task),
                "updates": updates,
            }
    except Exception as e:
        if "not found" in str(e).lower():
            raise
        logger.error(f"Error updating task: {str(e)}")
        raise Exception(f"Failed to update task: {str(e)}")


# ===========================================
# Export MCP tools
# ===========================================

# List of all MCP tools for easy import
__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
    "mcp",
]

# Tool metadata for manifest
TOOL_DEFINITIONS = [
    {
        "name": "add_task",
        "description": "Create a new task for the authenticated user",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title (1-255 characters)"},
                "description": {"type": "string", "description": "Optional task description (max 1000 characters)"},
            },
            "required": ["title"],
        },
    },
    {
        "name": "list_tasks",
        "description": "List all tasks for the authenticated user with optional status filter",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by status: 'all', 'pending', or 'completed'",
                    "enum": ["all", "pending", "completed"],
                    "default": "all",
                },
            },
        },
    },
    {
        "name": "complete_task",
        "description": "Mark a specific task as completed",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "UUID of the task to complete"},
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "delete_task",
        "description": "Remove a specific task from the user's list",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "UUID of the task to delete"},
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "update_task",
        "description": "Modify properties of an existing task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "UUID of the task to update"},
                "title": {"type": "string", "description": "New title (optional)"},
                "description": {"type": "string", "description": "New description (optional)"},
                "completed": {"type": "boolean", "description": "New completion status (optional)"},
            },
            "required": ["task_id"],
        },
    },
]
