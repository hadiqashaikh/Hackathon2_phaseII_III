"""
Chat API Router for Phase III: Todo AI Chatbot.

This module implements REST API endpoints for chat session and message management.
"""

import logging
import uuid
import traceback
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, Field

from database import get_session
from middleware.auth import get_current_user_id
from models import Conversation, Message, ConversationRead, MessageRead
from ai_agents.todo_agent import TodoAgentRunner, AgentResponse

# Set up logging with enhanced detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["chat"])


# ===========================================
# Request/Response Schemas
# ===========================================

class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID (UUID)")


class ToolCallResponse(BaseModel):
    """Schema for tool call information in response."""
    tool: str
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: str
    message: MessageRead
    tool_calls: List[ToolCallResponse] = []


class ConversationCreateResponse(BaseModel):
    """Response schema for creating a new conversation."""
    conversation_id: str
    session_id: str
    created_at: datetime


class MessageHistoryResponse(BaseModel):
    """Response schema for message history."""
    messages: List[MessageRead]
    count: int


# ===========================================
# Helper Functions
# ===========================================

def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def format_message_read(message: Message) -> MessageRead:
    """Convert Message model to MessageRead schema."""
    return MessageRead(
        id=message.id,
        conversation_id=message.conversation_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at,
    )


# ===========================================
# Chat Endpoints
# ===========================================

@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot and get a response.

    This endpoint:
    1. Validates authentication and extracts user_id
    2. Creates or retrieves a conversation
    3. Saves the user's message
    4. Processes the message with the AI agent
    5. Saves the AI's response
    6. Returns the response with any tool calls

    Args:
        request: Chat request with message and optional conversation_id
        user_id: Authenticated user's ID (from JWT token)
        session: Database session

    Returns:
        ChatResponse with conversation_id, AI message, and tool calls

    Raises:
        HTTPException: 404 if conversation not found or doesn't belong to user
    """
    logger.info("=" * 80)
    logger.info(f"CHAT REQUEST STARTED at {datetime.now().isoformat()}")
    logger.info(f"  user_id: {user_id}")
    logger.info(f"  request.message: {request.message[:100]}...")
    logger.info(f"  request.conversation_id: {request.conversation_id}")
    logger.debug(f"  Full request: {request.dict()}")

    # Step 1: Get or create conversation
    conversation = None
    session_id = None

    try:
        if request.conversation_id:
            # Verify conversation belongs to user
            try:
                conv_uuid = uuid.UUID(request.conversation_id)
            except (ValueError, AttributeError) as e:
                logger.error(f"  ✗ Invalid conversation_id format: {request.conversation_id}")
                logger.error(f"  Error: {type(e).__name__}: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation_id format"
                )

            logger.debug(f"  Fetching conversation: {conv_uuid}")
            conversation = session.exec(
                select(Conversation).where(
                    Conversation.id == conv_uuid,
                    Conversation.user_id == user_id
                )
            ).first()

            if not conversation:
                logger.warning(f"  ✗ Conversation {request.conversation_id} not found or not owned by user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )

            session_id = conversation.session_id
            logger.info(f"  ✓ Using existing Conversation: {conversation.id}")
        else:
            # Create new conversation
            session_id = generate_session_id()
            logger.debug(f"  Creating new conversation with session_id: {session_id}")
            conversation = Conversation(
                user_id=user_id,
                session_id=session_id
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"  ✓ Created new Conversation: {conversation.id}")

        # Step 2: Save user's message
        logger.debug(f"  Saving user message...")
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()
        logger.debug(f"  ✓ Saved user message: ID={user_message.id}")

        # Step 3: Fetch conversation history (last 10 messages to reduce token usage)
        logger.debug(f"  Fetching conversation history...")
        history_messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(10)  # Reduced from 15 to save tokens
        ).all()

        # Reverse to get chronological order
        history_messages = list(reversed(history_messages))
        logger.debug(f"  Retrieved {len(history_messages)} history messages")

        # Format for agent (exclude the message we just saved)
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages[:-1]  # Exclude the latest user message
        ]

        logger.debug(f"  ✓ Conversation history prepared: {len(conversation_history)} messages")
        logger.debug(f"  History preview: {conversation_history[-3:] if conversation_history else '[]'}")

        # Step 4: Process with AI agent
        logger.info(f"  → Calling TodoAgentRunner.process_message_sync()...")
        logger.debug(f"    - user_id: {user_id}")
        logger.debug(f"    - message: {request.message[:50]}...")
        logger.debug(f"    - conversation_history length: {len(conversation_history)}")
        
        try:
            runner = TodoAgentRunner(user_id=user_id)
            logger.debug(f"  ✓ TodoAgentRunner initialized")

            print(f'\n🤖 [CHAT ENDPOINT] Calling AI agent for user: {user_id}')
            print(f'   Message: "{request.message[:100]}..."')
            
            agent_response = runner.process_message_sync(
                message=request.message,
                conversation_history=conversation_history
            )
            print(f'   AI response received: "{agent_response.content[:100]}..."')
            print(f'   Tool calls: {len(agent_response.tool_calls)}\n')
            logger.info(f"  ✓ AI agent processing successful")
            logger.debug(f"    - agent_response.content: {agent_response.content[:100]}...")
            logger.debug(f"    - agent_response.tool_calls: {len(agent_response.tool_calls)} calls")
        except Exception as e:
            print(f'\n❌ [CHAT ENDPOINT] AI agent FAILED: {type(e).__name__}: {str(e)}\n')
            logger.error(f"  ✗ AI agent error: {type(e).__name__}: {str(e)}")
            logger.error(f"  Full traceback:\n{traceback.format_exc()}")
            # Rollback user message since we couldn't process it
            try:
                session.delete(user_message)
                session.commit()
            except Exception as rollback_error:
                logger.error(f"  Failed to rollback: {rollback_error}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI processing failed: {type(e).__name__}: {str(e)}"
            )

        # Step 5: Save AI's response
        logger.debug(f"  Saving AI response...")
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=agent_response.content
        )
        session.add(ai_message)
        session.commit()
        session.refresh(ai_message)
        logger.debug(f"  ✓ Saved AI message: ID={ai_message.id}")

        # Step 6: Format tool calls for response
        tool_call_responses = []
        for tc in agent_response.tool_calls:
            tool_call_responses.append(
                ToolCallResponse(
                    tool=tc.get("name", "unknown"),
                    result=tc.get("arguments", {})
                )
            )
            logger.debug(f"    - Tool call: {tc.get('name', 'unknown')} with args: {tc.get('arguments', {})}")

        logger.info(f"  ✓ Chat response generated. Tool calls: {len(tool_call_responses)}")

        # Step 7: Return response
        logger.info(f"CHAT REQUEST COMPLETED successfully")
        logger.info("=" * 80)
        
        return ChatResponse(
            conversation_id=str(conversation.id),
            message=format_message_read(ai_message),
            tool_calls=tool_call_responses
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (already logged)
        raise
    except Exception as e:
        # Catch any unexpected exceptions
        logger.error("=" * 80)
        logger.error(f"CHAT REQUEST FAILED with unexpected error")
        logger.error(f"  Error Type: {type(e).__name__}")
        logger.error(f"  Error Message: {str(e)}")
        logger.error(f"  Full traceback:\n{traceback.format_exc()}")
        logger.error("=" * 80)
        
        # Try to rollback user message if possible
        try:
            if 'user_message' in locals():
                session.delete(user_message)
                session.commit()
        except Exception as rollback_error:
            logger.error(f"  Failed to rollback user message: {rollback_error}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {type(e).__name__}: {str(e)}"
        )


@router.post("/conversations", response_model=ConversationCreateResponse)
def create_conversation(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new chat conversation.

    Args:
        user_id: Authenticated user's ID
        session: Database session

    Returns:
        ConversationCreateResponse with conversation details
    """
    logger.info(f"Creating new conversation for user_id: {user_id}")

    session_id = generate_session_id()
    conversation = Conversation(
        user_id=user_id,
        session_id=session_id
    )

    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    logger.info(f"Created Conversation: {conversation.id}")

    return ConversationCreateResponse(
        conversation_id=str(conversation.id),
        session_id=session_id,
        created_at=conversation.created_at
    )


@router.get("/conversations/{conversation_id}/messages", response_model=MessageHistoryResponse)
def get_conversation_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get message history for a specific conversation.

    Args:
        conversation_id: The conversation UUID
        user_id: Authenticated user's ID
        session: Database session

    Returns:
        MessageHistoryResponse with list of messages

    Raises:
        HTTPException: 404 if conversation not found or doesn't belong to user
    """
    logger.info(f"Fetching messages for conversation: {conversation_id}")

    # Verify conversation belongs to user
    try:
        conv_uuid = uuid.UUID(conversation_id)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation_id format"
        )

    conversation = session.exec(
        select(Conversation).where(
            Conversation.id == conv_uuid,
            Conversation.user_id == user_id
        )
    ).first()

    if not conversation:
        logger.warning(f"Conversation {conversation_id} not found or not owned by user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Fetch messages (ordered by creation time)
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conv_uuid)
        .order_by(Message.created_at.asc())
        .limit(50)
    ).all()

    logger.info(f"Retrieved {len(messages)} messages for conversation {conversation_id}")

    return MessageHistoryResponse(
        messages=[format_message_read(msg) for msg in messages],
        count=len(messages)
    )


@router.get("/conversations", response_model=List[ConversationRead])
def list_conversations(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List all conversations for the authenticated user.

    Args:
        user_id: Authenticated user's ID
        session: Database session

    Returns:
        List of conversations (most recent first)
    """
    logger.info(f"Listing conversations for user_id: {user_id}")

    conversations = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(20)
    ).all()

    logger.info(f"Retrieved {len(conversations)} conversations")

    return [
        ConversationRead(
            id=str(conv.id),  # Convert UUID to string for JSON serialization
            user_id=conv.user_id,
            session_id=conv.session_id,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: The conversation UUID
        user_id: Authenticated user's ID
        session: Database session

    Returns:
        Success confirmation

    Raises:
        HTTPException: 404 if conversation not found or doesn't belong to user
    """
    logger.info(f"Deleting conversation: {conversation_id}")

    # Verify conversation belongs to user
    try:
        conv_uuid = uuid.UUID(conversation_id)
        logger.debug(f"  Parsed UUID: {conv_uuid}")
    except (ValueError, AttributeError) as e:
        logger.error(f"  Invalid UUID format: {conversation_id} - {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation_id format"
        )

    try:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conv_uuid,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found or not owned by user {user_id}")
            # Get all conversations for this user to help debug
            user_convs = session.exec(
                select(Conversation).where(Conversation.user_id == user_id)
            ).all()
            logger.debug(f"  User has {len(user_convs)} conversations: {[str(c.id) for c in user_convs]}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation not found or access denied. You have {len(user_convs)} conversations."
            )

        # Delete conversation (messages cascade delete via foreign key)
        session.delete(conversation)
        session.commit()

        logger.info(f"Deleted Conversation: {conversation_id}")

        return {
            "success": True,
            "deleted_conversation_id": conversation_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {type(e).__name__}: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )
