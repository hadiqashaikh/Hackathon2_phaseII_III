"""
Tasks API Router - CRUD operations for tasks.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List

from models import Task, TaskCreate, TaskUpdate, TaskRead
from middleware.auth import get_current_user_id
from database import get_session_direct

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    request: Request,
    task: TaskCreate,
    user_id: str = Depends(get_current_user_id),
):
    """Create a new task."""
    logger.info(f"Creating task for user: {user_id}")
    
    session = get_session_direct()
    try:
        db_task = Task(
            id=str(__import__('uuid').uuid4()),
            title=task.title,
            completed=False,
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task
    except Exception as e:
        logger.error(f"Create task error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """List all tasks."""
    session = get_session_direct()
    try:
        logger.info(f"GET /api/tasks/ - user_id: {user_id}, cookies: {dict(request.cookies)}")
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
        ).all()
        logger.info(f"Found {len(tasks)} tasks for user {user_id}")
        return tasks
    except Exception as e:
        logger.error(f"Read tasks error: {e}")
        return []
    finally:
        session.close()


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: str,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Get a specific task."""
    session = get_session_direct()
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task
    finally:
        session.close()


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Update a task."""
    session = get_session_direct()
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task_update.title is not None:
            task.title = task_update.title
        if task_update.completed is not None:
            task.completed = task_update.completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return task
    except Exception as e:
        logger.error(f"Update task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Delete a task."""
    session = get_session_direct()
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()

        return {"message": "Task deleted"}
    except Exception as e:
        logger.error(f"Delete task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task(
    task_id: str,
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """Toggle task completion."""
    session = get_session_direct()
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.completed = not task.completed
        session.add(task)
        session.commit()
        session.refresh(task)

        return task
    except Exception as e:
        logger.error(f"Toggle task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
