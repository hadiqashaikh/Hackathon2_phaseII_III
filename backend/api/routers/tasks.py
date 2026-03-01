import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate, TaskRead
from security import get_current_user
from database import get_session
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    logger.info(f"Creating task for user_id: {user_id}")

    # Set the user_id from the token to ensure data isolation
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    logger.info(f"Task created successfully with id: {db_task.id}")
    return db_task

@router.get("/", response_model=List[TaskRead])
def read_tasks(current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    logger.info(f"Retrieving all tasks for user_id: {user_id}")

    # Filter tasks by the authenticated user's ID
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()

    logger.info(f"Retrieved {len(tasks)} tasks for user_id: {user_id}")
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: str, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    logger.info(f"Retrieving task {task_id} for user_id: {user_id}")

    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        logger.warning(f"Task {task_id} not found or not owned by user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Successfully retrieved task {task_id} for user_id: {user_id}")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    logger.info(f"Updating task {task_id} for user_id: {user_id}")

    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        logger.warning(f"Attempt to update non-existent or unauthorized task {task_id} by user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Store original values for logging
    original_values = {
        "title": db_task.title,
        "description": db_task.description,
        "completed": db_task.completed
    }

    # Update only the fields that are provided in the request
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    logger.info(f"Successfully updated task {task_id} for user_id: {user_id}")
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: str, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    logger.info(f"Deleting task {task_id} for user_id: {user_id}")

    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        logger.warning(f"Attempt to delete non-existent or unauthorized task {task_id} by user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    logger.info(f"Successfully deleted task {task_id} for user_id: {user_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task(task_id: str, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    logger.info(f"Toggling completion status for task {task_id} for user_id: {user_id}")

    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        logger.warning(f"Attempt to toggle non-existent or unauthorized task {task_id} by user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    original_status = db_task.completed
    # Toggle the completed status
    db_task.completed = not db_task.completed

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    logger.info(f"Successfully toggled task {task_id} completion status from {original_status} to {db_task.completed} for user_id: {user_id}")
    return db_task