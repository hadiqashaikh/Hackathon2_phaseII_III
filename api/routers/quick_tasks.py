"""
Quick Tasks API - Direct task operations without AI.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from models import Task, TaskRead
from middleware.auth import get_current_user_id
from database import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/quick-tasks", tags=["quick-tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    title: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a task directly."""
    task = Task(
        id=str(__import__('uuid').uuid4()),
        title=title,
        completed=False,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    status_filter: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """List tasks."""
    query = select(Task).where(Task.user_id == user_id)

    if status_filter == "completed":
        query = query.where(Task.completed == True)
    elif status_filter == "pending":
        query = query.where(Task.completed == False)

    tasks = session.exec(query.order_by(Task.created_at.desc())).all()
    return tasks


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
    return {"success": True}


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
