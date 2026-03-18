"""
MCP Tools for Task Management.
Fixed: No foreign key requirement, works with any user_id.
"""

import logging
import uuid
from typing import Optional, List, Dict, Any

from sqlmodel import Session, select
from models import Task
from database import get_session_direct
from mcp_server.context import MCPContext

logger = logging.getLogger(__name__)


def get_db_session() -> Session:
    """Get database session."""
    return get_session_direct()


def format_task(task: Task) -> Dict[str, Any]:
    """Format task for response."""
    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
    }


def add_task(ctx: MCPContext, title: str) -> Dict[str, Any]:
    """Create a new task."""
    logger.info(f"add_task called with user_id: '{ctx.user_id}', title: '{title}'")

    # Accept any non-empty user_id (including debug-user)
    if not ctx.user_id or ctx.user_id.strip() == "":
        logger.error("Unauthorized: User ID is empty or None")
        return {
            "success": False,
            "error": "User not authenticated. Please refresh the page and try again.",
            "requires_auth": True,
        }

    if not title or len(title.strip()) == 0:
        return {"success": False, "error": "Task title is required"}

    session = get_db_session()
    try:
        task = Task(
            id=str(uuid.uuid4()),
            title=title.strip(),
            completed=False,
            user_id=ctx.user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task created: {task.id} for user {ctx.user_id}")

        return {
            "success": True,
            "message": f'Task "{task.title}" created',
            "task": format_task(task),
        }
    except Exception as e:
        logger.error(f"Add task error: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Failed to create task: {str(e)}",
        }
    finally:
        session.close()


def list_tasks(ctx: MCPContext, status: str = "all") -> Dict[str, Any]:
    """List tasks with optional filter."""
    if not ctx.user_id:
        return {"success": False, "error": "Unauthorized", "tasks": [], "count": 0}

    session = get_db_session()
    try:
        query = select(Task).where(Task.user_id == ctx.user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        query = query.order_by(Task.created_at.desc())
        tasks = session.exec(query).all()

        return {
            "success": True,
            "message": f"Found {len(tasks)} {status} task(s)",
            "count": len(tasks),
            "tasks": [format_task(task) for task in tasks],
        }
    except Exception as e:
        logger.error(f"List tasks error: {e}")
        return {
            "success": False,
            "error": str(e),
            "tasks": [],
            "count": 0,
        }
    finally:
        session.close()


def complete_task(ctx: MCPContext, task_id: str) -> Dict[str, Any]:
    """Mark task as completed."""
    if not ctx.user_id:
        return {"success": False, "error": "Unauthorized"}

    session = get_db_session()
    try:
        logger.info(f"complete_task: Looking for task_id='{task_id}' for user='{ctx.user_id}'")

        # Try by ID first
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == ctx.user_id)
        ).first()

        # Try by exact title if not found by ID
        if not task:
            logger.info(f"complete_task: Not found by ID, trying exact title: '{task_id}'")
            task = session.exec(
                select(Task).where(
                    Task.user_id == ctx.user_id,
                    Task.title == task_id
                )
            ).first()

        # Try by partial title
        if not task:
            logger.info(f"complete_task: Not found by exact title, trying partial: '%{task_id}%'")
            task = session.exec(
                select(Task).where(
                    Task.user_id == ctx.user_id,
                    Task.title.ilike(f"%{task_id}%")
                )
            ).first()

        if not task:
            all_tasks = session.exec(
                select(Task).where(Task.user_id == ctx.user_id)
            ).all()
            logger.warning(f"complete_task: Task not found. User has {len(all_tasks)} tasks: {[t.title for t in all_tasks]}")
            return {"success": False, "error": f"Task not found: '{task_id}'"}

        if task.completed:
            return {
                "success": True,
                "message": f'Task "{task.title}" already completed',
                "task": format_task(task),
            }

        task.completed = True
        session.add(task)
        session.commit()

        return {
            "success": True,
            "message": f'Task "{task.title}" completed! Great job!',
            "task": format_task(task),
        }
    except Exception as e:
        logger.error(f"Complete task error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
    finally:
        session.close()


def delete_task(ctx: MCPContext, task_id: str) -> Dict[str, Any]:
    """Delete a task."""
    if not ctx.user_id:
        return {"success": False, "error": "Unauthorized"}

    session = get_db_session()
    try:
        logger.info(f"delete_task: Looking for task_id='{task_id}' for user='{ctx.user_id}'")

        # Try by ID first
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == ctx.user_id)
        ).first()

        # Try by exact title match
        if not task:
            logger.info(f"delete_task: Not found by ID, trying exact title match: '{task_id}'")
            task = session.exec(
                select(Task).where(
                    Task.user_id == ctx.user_id,
                    Task.title == task_id
                )
            ).first()

        # Try by partial title match
        if not task:
            logger.info(f"delete_task: Not found by exact title, trying partial match: '%{task_id}%'")
            task = session.exec(
                select(Task).where(
                    Task.user_id == ctx.user_id,
                    Task.title.ilike(f"%{task_id}%")
                )
            ).first()

        # List all tasks for debugging
        if not task:
            all_tasks = session.exec(
                select(Task).where(Task.user_id == ctx.user_id)
            ).all()
            logger.warning(f"delete_task: Task not found. User has {len(all_tasks)} tasks: {[t.title for t in all_tasks]}")

        if not task:
            return {"success": False, "error": f"Task not found: '{task_id}'"}

        task_title = task.title
        logger.info(f"delete_task: Found task '{task_title}' ({task.id}), deleting...")
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": f'Task "{task_title}" deleted',
            "deleted_id": task.id,
        }
    except Exception as e:
        logger.error(f"Delete task error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
    finally:
        session.close()


def update_task(
    ctx: MCPContext,
    task_id: str,
    title: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """Update a task."""
    if not ctx.user_id:
        return {"success": False, "error": "Unauthorized"}

    if title is None and completed is None:
        return {"success": False, "error": "At least one field must be provided"}

    session = get_db_session()
    try:
        logger.info(f"update_task: Looking for task_id='{task_id}' for user='{ctx.user_id}'")

        # Try by ID first
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == ctx.user_id)
        ).first()

        # Try by exact title
        if not task:
            logger.info(f"update_task: Not found by ID, trying exact title: '{task_id}'")
            task = session.exec(
                select(Task).where(
                    Task.user_id == ctx.user_id,
                    Task.title == task_id
                )
            ).first()

        # Try by partial title
        if not task:
            logger.info(f"update_task: Not found by exact title, trying partial: '%{task_id}%'")
            task = session.exec(
                select(Task).where(
                    Task.user_id == ctx.user_id,
                    Task.title.ilike(f"%{task_id}%")
                )
            ).first()

        if not task:
            all_tasks = session.exec(
                select(Task).where(Task.user_id == ctx.user_id)
            ).all()
            logger.warning(f"update_task: Task not found. User has {len(all_tasks)} tasks: {[t.title for t in all_tasks]}")
            return {"success": False, "error": f"Task not found: '{task_id}'"}

        if title is not None:
            task.title = title.strip()
        if completed is not None:
            task.completed = completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "message": f'Task "{task.title}" updated',
            "task": format_task(task),
        }
    except Exception as e:
        logger.error(f"Update task error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
    finally:
        session.close()


# Export for MCP
__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
]
