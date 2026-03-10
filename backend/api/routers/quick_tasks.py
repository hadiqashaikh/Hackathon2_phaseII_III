"""
Quick Task API - Direct task operations without AI.

Use these endpoints for instant task management instead of going through the AI chatbot.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate, TaskRead
from middleware.auth import get_current_user_id
from database import get_session
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(tags=["quick-tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    title: str,
    description: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a task directly without AI processing."""
    logger.info(f"Creating quick task for user_id: {user_id}, title: {title}")
    
    db_task = Task(
        title=title,
        description=description or "",
        completed=False,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    logger.info(f"Quick task created: {db_task.id}")
    return db_task


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    status_filter: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """List all tasks directly without AI processing."""
    logger.info(f"Listing quick tasks for user_id: {user_id}")
    
    query = select(Task).where(Task.user_id == user_id)
    
    if status_filter == "completed":
        query = query.where(Task.completed == True)
    elif status_filter == "pending":
        query = query.where(Task.completed == False)
    
    tasks = session.exec(query.order_by(Task.created_at.desc())).all()
    logger.info(f"Retrieved {len(tasks)} quick tasks")
    return tasks


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a task directly without AI processing."""
    logger.info(f"Deleting quick task {task_id} for user_id: {user_id}")
    
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    session.delete(task)
    session.commit()
    
    logger.info(f"Quick task deleted: {task_id}")
    return {"success": True, "deleted_task_id": task_id}


@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Toggle task completion status directly without AI processing."""
    logger.info(f"Toggling quick task {task_id} for user_id: {user_id}")
    
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    
    logger.info(f"Quick task toggled: {task_id}, completed: {task.completed}")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update a task directly without AI processing."""
    logger.info(f"Updating quick task {task_id} for user_id: {user_id}")
    
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    logger.info(f"Quick task updated: {task_id}")
    return task
