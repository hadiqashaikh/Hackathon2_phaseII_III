"""
Tasks API Router - CRUD operations for tasks.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from models import Task, TaskCreate, TaskUpdate, TaskRead
from middleware.auth import get_current_user_id
from database import get_session

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a new task."""
    logger.info(f"Creating task for user: {user_id}")

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


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """List all tasks."""
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    ).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get a specific task."""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update a task."""
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


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a task."""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted"}


@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Toggle task completion."""
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
