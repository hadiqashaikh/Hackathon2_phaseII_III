"""
FastAPI Backend for Todo AI Chatbot.
Production-ready, Hugging Face optimized.
"""

import sys
import io
import os
import logging
from typing import List

# UTF-8 encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

logger = logging.getLogger(__name__)

from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from database import engine, init_db
from config import settings

# Import routers
from routers import tasks
from routers import chat
from routers import quick_tasks
from middleware.auth import get_current_user_id, verify_session_token

# Create FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="AI-powered task management via natural language",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration - Explicit origins for cookie support
# When using credentials (cookies), we cannot use allow_origins=["*"]
# Must specify explicit origins
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

# Filter empty strings and strip whitespace
allowed_origins = [origin.strip() for origin in allowed_origins if origin.strip()]

# Default origins for local development and Vercel
if not allowed_origins:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

# Add Vercel preview and production domains
vercel_domains = os.getenv("VERCEL_ALLOWED_DOMAINS", "").split(",")
for domain in vercel_domains:
    domain = domain.strip()
    if domain:
        allowed_origins.append(f"https://{domain}")
        allowed_origins.append(f"https://{domain}.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with correct prefixes
# include_in_schema=False for auth routes (handled by Next.js)
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"], include_in_schema=False)
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


# ============================================================
# Better Auth Session Handler
# This handles /api/auth/get-session and other auth endpoints
# ============================================================

@app.get("/api/auth/get-session")
def get_session(request: Request):
    """
    Get current session from Better Auth cookies.
    Compatible with Better Auth client expectations.
    """
    # Get session token from cookies
    session_token = request.cookies.get("better-auth.session_token")
    
    if not session_token:
        # Try alternative cookie names
        session_token = request.cookies.get("better-auth.session-token")
    
    if not session_token:
        return {
            "session": None,
            "user": None,
        }
    
    # Verify session against database
    payload = verify_session_token(session_token)
    
    if not payload:
        return {
            "session": None,
            "user": None,
        }
    
    user_id = payload.get("id") or payload.get("userId") or payload.get("sub")
    
    return {
        "session": {
            "id": session_token,
            "userId": user_id,
        },
        "user": {
            "id": user_id,
            "userId": user_id,
        },
    }


@app.post("/api/auth/get-session")
def post_session(request: Request):
    """
    POST handler for get-session (Better Auth may use POST).
    """
    return get_session(request)
