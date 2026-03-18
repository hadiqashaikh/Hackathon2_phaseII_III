"""
SQLModel definitions for Todo AI Chatbot.
"""

from sqlmodel import SQLModel, Field, Column
from typing import Optional
import uuid
from datetime import datetime
from sqlalchemy import DateTime


# ===========================================
# Task Models
# ===========================================

class Task(SQLModel, table=True):
    """Task table - matches Neon DB schema."""
    __tablename__ = "task"
    __table_args__ = {"extend_existing": True}

    id: str = Field(primary_key=True)
    user_id: str = Field(sa_column=Column("userId", index=True))
    title: str = Field(min_length=1, max_length=255)
    completed: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("createdAt", DateTime(timezone=True))
    )


class TaskCreate(SQLModel):
    """Schema for creating a task."""
    title: str = Field(min_length=1, max_length=255)


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    completed: Optional[bool] = Field(default=None)


class TaskRead(SQLModel):
    """Schema for returning task data."""
    id: str
    title: str
    completed: bool
    user_id: str
    created_at: datetime


# ===========================================
# Conversation Models
# ===========================================

class Conversation(SQLModel, table=True):
    """Chat conversation session."""
    __tablename__ = "conversation"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)
    session_id: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Chat message."""
    __tablename__ = "message"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id",
        ondelete="CASCADE",
        index=True
    )
    role: str  # user, assistant, system
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationRead(SQLModel):
    """Schema for returning conversation data."""
    id: uuid.UUID
    user_id: str
    session_id: str
    created_at: datetime
    updated_at: datetime


class MessageRead(SQLModel):
    """Schema for returning message data."""
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    created_at: datetime


# ===========================================
# User Models (for Better Auth)
# ===========================================

class User(SQLModel, table=True):
    """User table for Better Auth."""
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    email_verified: bool = Field(default=False)
    name: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
