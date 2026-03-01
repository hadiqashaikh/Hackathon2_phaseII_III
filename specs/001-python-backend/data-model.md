# Data Model: Task Management System

## Overview
This document defines the SQLModel database schema for the task management system, with a focus on multi-tenancy through user_id isolation. The design ensures that all user data is properly isolated and accessible only to the authenticated user who owns it.

## Database Schema

### Task Model
```python
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Critical for multi-tenancy
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Description**: Represents a user's task with all necessary fields for management and tracking.

**Key Constraints**:
- `user_id` field is indexed for efficient filtering and querying
- `title` must be between 1 and 255 characters
- `description` optional, up to 1000 characters
- `completed` defaults to False for new tasks
- `created_at` and `updated_at` automatically managed by the system

### Entity Relationships
```
User (JWT Token) -> Task (via user_id)
```
The relationship is implicit through the user_id field in the Task table, which corresponds to the user_id extracted from the JWT token.

## SQLModel Implementation

### Python Schema Definition
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

## Multi-tenancy Considerations

### User Data Isolation
- All queries must include a filter: `where(Task.user_id == current_user_id)`
- The user_id is extracted from the authenticated JWT token
- No task should be accessible without proper authentication

### Access Control Patterns
```python
# Example of safe query that ensures multi-tenancy
def get_user_tasks(user_id: str, session: Session):
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

def get_task_by_id(task_id: uuid.UUID, user_id: str, session: Session):
    return session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
```

### Security Requirements
- Any query without user_id filtering is a potential security vulnerability
- All API endpoints must validate that URL parameters match the authenticated user
- No direct access to tasks without authentication

## Database Indexing Strategy

### Required Indexes
- `user_id`: Primary index for filtering tasks by authenticated user (critical for multi-tenancy)
- `created_at`: For time-based queries and sorting
- Composite index on `(user_id, created_at)`: For efficient queries of user's tasks sorted by creation date

### Performance Considerations
- Indexes ensure O(log n) lookup for user-specific queries
- Proper indexing prevents full table scans on large datasets
- Consider partial indexes if needed for completed vs. incomplete tasks

## API Integration Points

### Task Creation
- When creating a task, the user_id will be automatically set from the JWT token
- No user_id is accepted from the request body to prevent data isolation breaches

### Task Retrieval
- All GET endpoints will filter based on the authenticated user's ID
- Individual task access will validate both task existence and ownership

### Task Updates
- Updates will first verify ownership using user_id from token
- Prevents unauthorized modification of other users' tasks

### Task Deletion
- Deletion will first verify ownership and existence
- Prevents unauthorized deletion of other users' tasks

## Validation Rules

### Input Validation
- Title: Required, 1-255 characters
- Description: Optional, up to 1000 characters
- Completed: Boolean value only

### Business Logic Validation
- Users can only modify their own tasks
- Task IDs must exist and belong to the authenticated user
- No external modification of user_id field

## Security Considerations

### Data Isolation
- Primary defense: WHERE clause filtering by user_id on all queries
- Secondary defense: Validation that URL parameters match token user_id
- Regular security audits to ensure no query bypasses user_id filtering

### Token Validation
- JWT tokens must be properly validated before any database access
- Expired tokens must be rejected
- User_id from token must match expected values

### Error Handling
- Generic error messages to prevent information disclosure
- Proper HTTP status codes (401, 403, 404) without revealing data existence
- Log security-related events appropriately