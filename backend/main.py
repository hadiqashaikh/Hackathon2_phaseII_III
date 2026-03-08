"""
FastAPI Backend for Phase III: Todo AI Chatbot.

This backend extends the Phase II Task API with AI-powered chat functionality
using OpenAI Agents SDK and Model Context Protocol (MCP).
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine, init_db
from config import settings

# Import routers
from api.routers import tasks
from api.routers import chat

# Import authentication dependencies
from middleware.auth import get_current_user_id

# Initialize FastAPI app with Phase III metadata
app = FastAPI(
    title="Todo AI Chatbot API",
    description="FastAPI backend with AI-powered task management via natural language",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS with explicit localhost:3000 origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)

# Include Phase II task router (backward compatibility)
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

# Include Phase III chat router (AI chatbot)
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()


@app.get("/")
def read_root():
    """Root endpoint - API health check."""
    return {
        "message": "Todo AI Chatbot API is running!",
        "version": "3.0.0",
        "phase": "III",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "phase": "III"}


# ===========================================
# Authentication Test Endpoints (Phase III)
# ===========================================

@app.get("/api/auth/me")
def get_current_user_info(user_id: str = Depends(get_current_user_id)):
    """
    Get current authenticated user information.
    
    This endpoint demonstrates the auth middleware in action.
    Returns 401 if not authenticated, or user_id if authenticated.
    """
    return {
        "user_id": user_id,
        "authenticated": True,
    }


@app.get("/api/protected")
def get_protected_resource(user_id: str = Depends(get_current_user_id)):
    """
    Example protected endpoint that requires authentication.
    
    The user_id is automatically extracted from the JWT token
    by the auth middleware.
    """
    return {
        "message": "You have access to this protected resource",
        "user_id": user_id,
    }
