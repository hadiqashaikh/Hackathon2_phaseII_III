"""
FastAPI Backend for Todo AI Chatbot.
Production-ready, Hugging Face optimized.
"""

import sys
import io

# UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from database import engine, init_db
from config import settings

# Import routers
from api.routers import tasks
from api.routers import chat
from api.routers import quick_tasks
from middleware.auth import get_current_user_id

# Create FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="AI-powered task management via natural language",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*",  # Allow all for Hugging Face deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with correct prefixes
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(quick_tasks.router, prefix="/api/quick-tasks", tags=["quick-tasks"])


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    init_db()
    print("✓ Database initialized")
    print(f"✓ DEBUG MODE: {settings.DEBUG}")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Todo AI Chatbot API is running!",
        "version": "3.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "phase": "III"}


@app.get("/api/auth/me")
def get_current_user(user_id: str = Depends(get_current_user_id)):
    """Get current user info."""
    return {
        "user_id": user_id,
        "authenticated": True,
    }
