"""
SQLModel models for Phase III: Todo AI Chatbot.

This module defines all database models including:
- Task (Phase II): Existing task management model (matches Neon DB schema)
- Conversation (Phase III): Chat session tracking
- Message (Phase III): Individual chat messages
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime
from sqlalchemy import Column


# ===========================================
# Task Models (Phase II - Existing)
# ===========================================
# IMPORTANT: This model must match the existing Neon DB schema from Phase II
# Database columns: id (TEXT), userId (TEXT), title (TEXT), completed (BOOLEAN), createdAt (TIMESTAMP)

class TaskBase(SQLModel):
    """Base schema for task operations."""
    title: str = Field(min_length=1, max_length=255, description="Task title")
    completed: bool = Field(default=False, description="Task completion status")
    user_id: str = Field(description="Owner of the task (for multi-tenancy)")


class Task(TaskBase, table=True):
    """
    Task table model - matches existing Phase II Neon DB schema.
    
    Database uses camelCase column names: userId, createdAt
    """
    __tablename__ = "task"
    __table_args__ = {"extend_existing": True}
    
    # Map Python attribute names to database column names
    id: str = Field(primary_key=True)
    user_id: str = Field(sa_column=Column("userId", index=True))
    title: str = Field(min_length=1, max_length=255)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column("createdAt"))


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    completed: Optional[bool] = Field(default=None)


class TaskRead(TaskBase):
    """Schema for returning task data."""
    id: str
    created_at: datetime


# ===========================================
# Conversation Models (Phase III - New)
# ===========================================

class ConversationBase(SQLModel):
    """Base schema for conversation sessions."""
    user_id: str = Field(
        index=True,
        description="Owner of this conversation (references Better Auth user)"
    )


class Conversation(ConversationBase, table=True):
    """
    Conversation session for tracking AI chat history.
    
    Each conversation represents a unique chat session for a user.
    Messages are linked to conversations via foreign key.
    """
    __tablename__ = "conversation"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique conversation identifier"
    )
    session_id: str = Field(
        unique=True,
        index=True,
        description="Unique session identifier (UUID string)"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Conversation creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Conversation last update timestamp"
    )
    
    # Relationship to messages (one-to-many)
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ConversationRead(SQLModel):
    """Schema for returning conversation data."""
    id: str  # Return as string for JSON serialization
    user_id: str
    session_id: str
    created_at: datetime
    updated_at: datetime


# ===========================================
# Message Models (Phase III - New)
# ===========================================

class MessageBase(SQLModel):
    """Base schema for chat messages."""
    role: str = Field(
        description="Message role: 'user', 'assistant', or 'system'"
    )
    content: str = Field(
        description="Message content text"
    )


class Message(MessageBase, table=True):
    """
    Individual message within a conversation.
    
    Each message belongs to exactly one conversation and has a role
    indicating whether it was sent by the user or the AI assistant.
    """
    __tablename__ = "message"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique message identifier"
    )
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id",
        index=True,
        description="Reference to parent conversation"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp"
    )
    
    # Relationship to conversation (many-to-one)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    """Schema for returning message data."""
    id: uuid.UUID
    conversation_id: uuid.UUID
    created_at: datetime


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass
