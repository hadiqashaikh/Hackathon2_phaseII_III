# Quickstart Guide: FastAPI Backend with JWT Verification

## Overview
This guide provides step-by-step instructions to set up the FastAPI backend with JWT token verification and SQLModel for task management, ensuring compatibility with Better Auth tokens and proper user data isolation.

## Prerequisites
- Python 3.10 or higher installed
- pip package manager
- Access to a Neon PostgreSQL database instance
- The same BETTER_AUTH_SECRET used by the frontend Better Auth system

## Step 1: Setup Python Environment

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlmodel python-jose[cryptography] psycopg2-binary
```

## Step 2: Create Project Structure

Create the following directory structure:

```
backend/
├── main.py
├── models.py
├── database.py
├── security.py
├── api/
│   └── routers/
│       └── tasks.py
├── requirements.txt
└── .env
```

## Step 3: Create requirements.txt

```txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
sqlmodel==0.0.26
python-jose[cryptography]==3.3.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
```

## Step 4: Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/db_name
BETTER_AUTH_SECRET=your_32_character_secret_key_here_must_be_at_least_32_characters
```

## Step 5: Create Database Connection

Create `database.py`:

```python
from sqlmodel import create_engine, Session
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

## Step 6: Define Models

Create `models.py`:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Critical for data isolation

class Task(TaskBase, table=True):
    """Task model with user_id for multi-tenancy."""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)

class TaskRead(TaskBase):
    """Schema for returning task data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

## Step 7: Implement Security Layer

Create `security.py`:

```python
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from models import Task
from database import get_session
from jose import JWTError, jwt
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

ALGORITHM = "HS256"

def verify_token(token: str) -> dict:
    """Verify JWT token and extract user information."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Check if token is expired
    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
        raise credentials_exception

    return payload

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token."""
    return verify_token(credentials.credentials)

def verify_user_owns_task(user_id: str, task: Task) -> None:
    """Verify that the user owns the task."""
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
```

## Step 8: Create Task Router

Create `api/routers/tasks.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate, TaskRead
from security import get_current_user
from database import get_session
from typing import List

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    # Set the user_id from the token to ensure data isolation
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user["id"]
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskRead])
def read_tasks(current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    # Filter tasks by the authenticated user's ID
    user_id = current_user["id"]
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: str, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

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
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: str, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
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
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task(task_id: str, current_user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user["id"]
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completed status
    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

## Step 9: Create Main Application

Create `main.py`:

```python
from fastapi import FastAPI
from api.routers import tasks
from sqlmodel import SQLModel
from database import engine

app = FastAPI(title="FastAPI Task Backend", version="1.0.0")

# Include the task router
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    # Create database tables
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI Task Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Step 10: Run the Application

```bash
cd backend
uvicorn main:app --reload
```

The server will start on http://localhost:8000.

## Step 11: Test the API

Use curl or a tool like Postman to test the API:

```bash
# Get API docs (auto-generated by FastAPI)
curl http://localhost:8000/docs

# Test an authenticated endpoint (replace YOUR_TOKEN with a valid Better Auth JWT)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -X GET http://localhost:8000/api/tasks/
```

## Verification Checklist

- [ ] Python virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Environment variables properly configured
- [ ] Database connection established
- [ ] JWT token validation working
- [ ] User data isolation enforced (user_id filtering)
- [ ] All 6 task endpoints functional (create, read list, read single, update, delete, toggle)
- [ ] Authentication required for all task endpoints
- [ ] Requests without valid Bearer token return 401 Unauthorized