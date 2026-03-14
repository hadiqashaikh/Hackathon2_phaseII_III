"""
Chat API Router - AI chatbot for natural language task management.
Fixed: ForeignKeyViolation, POST response, session/user context, UUID casting.
"""

import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete
from pydantic import BaseModel

from models import Conversation, Message, ConversationRead, MessageRead
from middleware.auth import get_current_user_id
from database import get_session
from ai_agents.openrouter_agent import OpenRouterAgent
from config import settings

logger = logging.getLogger(__name__)

# NO prefix here - prefix is set in main.py
router = APIRouter(tags=["chat"])


def get_debug_user_id() -> str:
    """Get debug user ID for development when auth is not available."""
    return "debug-user-id"


class ChatMessage(BaseModel):
    """Chat request."""
    message: str
    conversation_id: Optional[str] = None


class MessageResponse(BaseModel):
    """Single message response."""
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: str


class ChatResponse(BaseModel):
    """Chat response - matches frontend expectation."""
    conversation_id: str
    message: MessageResponse
    tool_calls: List[Dict[str, Any]] = []


class ConversationDeleteResponse(BaseModel):
    """Delete conversation response."""
    success: bool
    message: str


# ✅ POST /api/chat/message
@router.post("/message")
def chat_message(
    chat_request: ChatMessage,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Send a message to the AI chatbot."""
    logger.info(f"Chat message from user: {user_id}, message: {chat_request.message[:50]}...")
    logger.info(f"DEBUG: user_id type={type(user_id)}, value='{user_id}', bool={bool(user_id)}")

    try:
        # Get or create conversation
        conversation = None
        if chat_request.conversation_id:
            # Cast to UUID for database query
            try:
                conv_uuid = uuid.UUID(chat_request.conversation_id)
                conversation = session.exec(
                    select(Conversation).where(
                        Conversation.id == conv_uuid,
                        Conversation.user_id == user_id
                    )
                ).first()
            except (ValueError, AttributeError):
                conversation = session.exec(
                    select(Conversation).where(
                        Conversation.session_id == chat_request.conversation_id,
                        Conversation.user_id == user_id
                    )
                ).first()

        if not conversation:
            conversation = Conversation(
                user_id=user_id,
                session_id=str(uuid.uuid4())
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"Created new conversation: {conversation.session_id}")

        # Get conversation history (last 10 messages)
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(10)
        ).all()

        history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(messages)
        ]

        # Process with AI agent - wrapped in try-except
        try:
            logger.info(f"Creating OpenRouterAgent with user_id: '{user_id}'")
            agent = OpenRouterAgent(user_id=user_id)
            logger.info(f"OpenRouterAgent.user_id: '{agent.user_id}'")
            response = agent.process_message(
                message=chat_request.message,
                history=history
            )
        except Exception as ai_error:
            logger.error(f"AI Agent error: {type(ai_error).__name__}: {str(ai_error)}")
            # Return a fallback response instead of crashing
            response_content = f"I apologize, but I'm having trouble connecting to the AI service. Error: {str(ai_error)}"
            response = type('obj', (object,), {'content': response_content, 'tool_calls': []})

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message
        )
        session.add(user_msg)

        # Save AI response
        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response.content
        )
        session.add(assistant_msg)
        session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        logger.info(f"Chat response sent, tool_calls: {len(response.tool_calls) if response.tool_calls else 0}")

        # Return structure matching frontend expectation
        return {
            "conversation_id": conversation.session_id,
            "message": {
                "id": str(assistant_msg.id),
                "conversation_id": conversation.session_id,
                "role": "assistant",
                "content": response.content,
                "created_at": assistant_msg.created_at.isoformat()
            },
            "tool_calls": response.tool_calls if response.tool_calls else []
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


# ✅ GET /api/chat/conversations
@router.get("/conversations", response_model=List[ConversationRead])
def list_conversations(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """List all conversations."""
    try:
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).all()
        return conversations
    except Exception as e:
        logger.error(f"List conversations error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list conversations: {str(e)}"
        )


# ✅ GET /api/chat/conversations/{session_id}
@router.get("/conversations/{session_id}")
def get_conversation(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get a conversation with all its messages."""
    try:
        # Try to find by session_id (string)
        conversation = session.exec(
            select(Conversation).where(
                Conversation.session_id == session_id,
                Conversation.user_id == user_id
            )
        ).first()
        
        # If not found, try by UUID
        if not conversation:
            try:
                conv_uuid = uuid.UUID(session_id)
                conversation = session.exec(
                    select(Conversation).where(
                        Conversation.id == conv_uuid,
                        Conversation.user_id == user_id
                    )
                ).first()
            except ValueError:
                pass

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
        ).all()

        return {
            "conversation": conversation,
            "messages": messages,
            "count": len(messages)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get conversation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation: {str(e)}"
        )


# ✅ GET /api/chat/conversations/{session_id}/messages
@router.get("/conversations/{session_id}/messages")
def get_conversation_messages(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get all messages for a conversation."""
    logger.info(f"Getting messages for conversation: {session_id}")
    
    try:
        # Try to find by session_id (string)
        conversation = session.exec(
            select(Conversation).where(
                Conversation.session_id == session_id,
                Conversation.user_id == user_id
            )
        ).first()
        
        # If not found, try by UUID
        if not conversation:
            try:
                conv_uuid = uuid.UUID(session_id)
                conversation = session.exec(
                    select(Conversation).where(
                        Conversation.id == conv_uuid,
                        Conversation.user_id == user_id
                    )
                ).first()
                if conversation:
                    logger.info(f"Found conversation by UUID: {conversation.id}")
            except ValueError:
                pass
        
        if not conversation:
            logger.warning(f"Conversation not found: {session_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
        ).all()

        return {
            "conversation_id": conversation.session_id,
            "messages": messages,
            "count": len(messages)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get messages error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )


# ✅ DELETE /api/chat/conversations/{session_id}
@router.delete("/conversations/{session_id}", response_model=ConversationDeleteResponse)
def delete_conversation(
    session_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a conversation and all its messages using CASCADE."""
    logger.info(f"Deleting conversation: {session_id}")

    try:
        # Try to find by session_id (string) FIRST
        conversation = session.exec(
            select(Conversation).where(
                Conversation.session_id == session_id,
                Conversation.user_id == user_id
            )
        ).first()

        # If not found, try by UUID
        if not conversation:
            try:
                conv_uuid = uuid.UUID(session_id)
                conversation = session.exec(
                    select(Conversation).where(
                        Conversation.id == conv_uuid,
                        Conversation.user_id == user_id
                    )
                ).first()
                if conversation:
                    logger.info(f"Found conversation by UUID: {conversation.id}")
            except ValueError:
                pass

        if not conversation:
            logger.warning(f"Conversation not found: {session_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found. It may have already been deleted."
            )

        # Delete all messages first using SQL DELETE statement
        # This bypasses the foreign key constraint issue
        deleted_messages = session.exec(
            delete(Message).where(Message.conversation_id == conversation.id)
        )
        logger.info(f"Deleted {deleted_messages} messages for conversation {session_id}")

        # Now delete the conversation
        session.delete(conversation)
        session.commit()

        logger.info(f"Deleted conversation: {session_id}")

        return ConversationDeleteResponse(
            success=True,
            message="Conversation deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete conversation error: {e}", exc_info=True)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )
