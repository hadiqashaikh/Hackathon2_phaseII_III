"""
Debug API for Phase III: Todo AI Chatbot.

This module provides enhanced logging and debugging capabilities for the chat API.
Run this instead of main.py to get detailed error diagnostics.

Supports both OpenAI and OpenRouter API endpoints.
"""

import logging
import sys
import traceback
from datetime import datetime

# Configure detailed logging BEFORE any other imports
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Log startup with timestamp
logger.info("=" * 80)
logger.info(f"DEBUG_API STARTING at {datetime.now().isoformat()}")
logger.info("=" * 80)

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from database import engine, init_db, get_session_direct
from config import settings

# Import routers
from api.routers import tasks
from api.routers import chat

# Import authentication dependencies
from middleware.auth import get_current_user_id

# ===========================================
# Environment Variable Diagnostics
# ===========================================

logger.info("DIAGNOSTIC: Checking environment variables...")
logger.info(f"  DATABASE_URL present: {bool(settings.DATABASE_URL)}")
logger.info(f"  DATABASE_URL preview: {settings.DATABASE_URL[:30]}..." if settings.DATABASE_URL else "  DATABASE_URL: MISSING")
logger.info(f"  BETTER_AUTH_SECRET present: {bool(settings.BETTER_AUTH_SECRET)}")
logger.info(f"  OPENAI_API_KEY present: {bool(settings.OPENAI_API_KEY)}")
logger.info(f"  OPENAI_API_KEY preview: {settings.OPENAI_API_KEY[:15]}..." if settings.OPENAI_API_KEY else "  OPENAI_API_KEY: MISSING")
logger.info(f"  OPENAI_BASE_URL: {settings.OPENAI_BASE_URL}")
logger.info(f"  OPENAI_AGENT_MODEL: {settings.OPENAI_AGENT_MODEL}")
logger.info(f"  BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")

# Detect if using OpenRouter
is_openrouter = "openrouter.ai" in settings.OPENAI_BASE_URL
logger.info(f"  Provider: {'OpenRouter' if is_openrouter else 'OpenAI'}")

# Test database connectivity
logger.info("DIAGNOSTIC: Testing database connectivity...")
try:
    test_session = get_session_direct()
    try:
        from sqlalchemy import text
        test_session.exec(text("SELECT 1"))
        logger.info("  ✓ Database connection successful")
    finally:
        test_session.close()
except Exception as e:
    logger.error(f"  ✗ Database connection FAILED: {type(e).__name__}: {str(e)}")
    logger.error(f"  Full traceback:\n{traceback.format_exc()}")

# Test OpenAI/OpenRouter API key validity
logger.info(f"DIAGNOSTIC: Testing {'OpenRouter' if is_openrouter else 'OpenAI'} API key...")
if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "sk-placeholder-for-migration":
    logger.info(f"  ✓ API key is set (not a placeholder)")
    try:
        import openai
        
        # Configure client with OpenRouter support
        if is_openrouter:
            logger.info(f"  Using OpenRouter base_url: {settings.OPENAI_BASE_URL}")
            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Todo AI Chatbot",
                }
            )
        else:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Try a minimal API call to validate the key
        models = client.models.list()
        model_list = [m.id for m in list(models)[:10]]
        logger.info(f"  ✓ API key is valid - found {len(model_list)} models")
        logger.info(f"  Available models (first 10): {model_list}")
        
        # Check if target model is available
        if settings.OPENAI_AGENT_MODEL in model_list or any(settings.OPENAI_AGENT_MODEL in m for m in model_list):
            logger.info(f"  ✓ Target model '{settings.OPENAI_AGENT_MODEL}' is available")
        else:
            logger.warning(f"  ⚠ Target model '{settings.OPENAI_AGENT_MODEL}' not found in first 10 models")
            
    except openai.AuthenticationError as e:
        logger.error(f"  ✗ API key is INVALID: {type(e).__name__}: {str(e)}")
        logger.error(f"  Full traceback:\n{traceback.format_exc()}")
    except Exception as e:
        logger.error(f"  ? API key test error: {type(e).__name__}: {str(e)}")
        logger.error(f"  Full traceback:\n{traceback.format_exc()}")
else:
    logger.error(f"  ✗ API key is missing or placeholder!")
    logger.error(f"  Please update .env file with a valid API key")
    if is_openrouter:
        logger.error(f"  Get your OpenRouter key at: https://openrouter.ai/keys")
    else:
        logger.error(f"  Get your OpenAI key at: https://platform.openai.com/api-keys")

logger.info("=" * 80)

# Initialize FastAPI app with Phase III metadata
app = FastAPI(
    title="Todo AI Chatbot API (DEBUG MODE)",
    description="FastAPI backend with AI-powered task management via natural language - WITH ENHANCED LOGGING",
    version="3.0.0-DEBUG",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS with settings from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)


# ===========================================
# Global Exception Handler
# ===========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler to log all unhandled exceptions.
    """
    logger.error("=" * 80)
    logger.error(f"GLOBAL EXCEPTION CAUGHT at {datetime.now().isoformat()}")
    logger.error(f"  Request: {request.method} {request.url}")
    logger.error(f"  Exception Type: {type(exc).__name__}")
    logger.error(f"  Exception Message: {str(exc)}")
    logger.error(f"  Full Traceback:\n{traceback.format_exc()}")
    logger.error("=" * 80)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "type": type(exc).__name__,
            "message": str(exc),
            "debug_mode": True
        }
    )


# Include Phase II task router (backward compatibility)
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

# Include Phase III chat router (AI chatbot) - with debugging wrapper
logger.info("Wrapping chat router with enhanced logging...")
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.on_event("startup")
async def on_startup():
    """Initialize database tables on application startup with diagnostics."""
    logger.info("DIAGNOSTIC: Initializing database...")
    try:
        init_db()
        logger.info("  ✓ Database initialization successful")
    except Exception as e:
        logger.error(f"  ✗ Database initialization FAILED: {type(e).__name__}: {str(e)}")
        logger.error(f"  Full traceback:\n{traceback.format_exc()}")
        raise


@app.get("/")
def read_root():
    """Root endpoint - API health check with diagnostics."""
    return {
        "message": "Todo AI Chatbot API is running (DEBUG MODE)!",
        "version": "3.0.0-DEBUG",
        "phase": "III",
        "docs": "/docs",
        "diagnostics": {
            "database_url_present": bool(settings.DATABASE_URL),
            "openai_api_key_present": bool(settings.OPENAI_API_KEY),
            "openai_base_url": settings.OPENAI_BASE_URL,
            "openai_agent_model": settings.OPENAI_AGENT_MODEL,
            "provider": "OpenRouter" if is_openrouter else "OpenAI",
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint with detailed diagnostics."""
    health_status = {
        "status": "healthy",
        "phase": "III",
        "debug_mode": True,
        "checks": {}
    }
    
    # Check database
    try:
        session = get_session_direct()
        try:
            from sqlalchemy import text
            session.exec(text("SELECT 1"))
            health_status["checks"]["database"] = "connected"
        finally:
            session.close()
    except Exception as e:
        health_status["checks"]["database"] = f"FAILED: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check OpenAI/OpenRouter
    try:
        import openai
        
        if is_openrouter:
            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Todo AI Chatbot",
                }
            )
        else:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        client.models.list()
        health_status["checks"]["openai"] = "connected"
    except Exception as e:
        health_status["checks"]["openai"] = f"FAILED: {str(e)}"
        health_status["status"] = "unhealthy"
    
    return health_status


# ===========================================
# Debug-specific Endpoints
# ===========================================

@app.get("/debug/config")
def debug_config():
    """Return current configuration (safe for debugging)."""
    return {
        "DATABASE_URL_present": bool(settings.DATABASE_URL),
        "DATABASE_URL_preview": f"{settings.DATABASE_URL[:30]}..." if settings.DATABASE_URL else None,
        "BETTER_AUTH_SECRET_present": bool(settings.BETTER_AUTH_SECRET),
        "OPENAI_API_KEY_present": bool(settings.OPENAI_API_KEY),
        "OPENAI_API_KEY_preview": f"{settings.OPENAI_API_KEY[:15]}..." if settings.OPENAI_API_KEY else None,
        "OPENAI_BASE_URL": settings.OPENAI_BASE_URL,
        "OPENAI_AGENT_MODEL": settings.OPENAI_AGENT_MODEL,
        "BACKEND_CORS_ORIGINS": settings.BACKEND_CORS_ORIGINS,
        "provider": "OpenRouter" if is_openrouter else "OpenAI",
    }


@app.get("/debug/test-db")
def debug_test_db():
    """Test database connectivity."""
    result = {
        "success": False,
        "error": None,
        "details": {}
    }
    
    try:
        session = get_session_direct()
        try:
            from sqlalchemy import text
            query_result = session.exec(text("SELECT 1 as test"))
            result["success"] = True
            result["details"] = {"query_result": list(query_result)}
        finally:
            session.close()
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)}"
        result["traceback"] = traceback.format_exc()
    
    return result


@app.get("/debug/test-openai")
def debug_test_openai():
    """Test OpenAI/OpenRouter API connectivity."""
    result = {
        "success": False,
        "error": None,
        "details": {}
    }
    
    if not settings.OPENAI_API_KEY:
        result["error"] = "OPENAI_API_KEY not set"
        return result
    
    if settings.OPENAI_API_KEY == "sk-placeholder-for-migration":
        result["error"] = "OPENAI_API_KEY is still a placeholder"
        return result
    
    try:
        import openai
        
        # Configure client with OpenRouter support
        if is_openrouter:
            logger.info(f"Using OpenRouter: {settings.OPENAI_BASE_URL}")
            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Todo AI Chatbot",
                }
            )
        else:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        models = client.models.list()
        model_list = [m.id for m in list(models)[:10]]
        result["success"] = True
        result["details"] = {
            "provider": "OpenRouter" if is_openrouter else "OpenAI",
            "base_url": settings.OPENAI_BASE_URL,
            "available_models": model_list,
            "target_model": settings.OPENAI_AGENT_MODEL,
            "model_available": settings.OPENAI_AGENT_MODEL in model_list or any(settings.OPENAI_AGENT_MODEL in m for m in model_list)
        }
    except openai.AuthenticationError as e:
        result["error"] = f"Authentication failed: {str(e)}"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)}"
        result["traceback"] = traceback.format_exc()
    
    return result


@app.get("/debug/test-agent")
def debug_test_agent():
    """Test TodoAgent initialization."""
    result = {
        "success": False,
        "error": None,
        "details": {}
    }
    
    try:
        from ai_agents.todo_agent import TodoAgentRunner, create_todo_agent
        
        # Test agent creation
        logger.info("DEBUG: Creating agent...")
        agent = create_todo_agent()
        logger.info(f"DEBUG: Agent created: {agent.name}")
        
        # Test runner initialization
        logger.info("DEBUG: Creating runner with test user_id...")
        runner = TodoAgentRunner(user_id="debug-user-123")
        logger.info(f"DEBUG: Runner created successfully")
        
        result["success"] = True
        result["details"] = {
            "agent_name": agent.name,
            "agent_model": agent.model,
            "base_url": settings.OPENAI_BASE_URL,
            "provider": "OpenRouter" if is_openrouter else "OpenAI",
            "tools_count": len(agent.tools) if hasattr(agent.tools, '__len__') else "N/A",
        }
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)}"
        result["traceback"] = traceback.format_exc()
        logger.error(f"DEBUG: Agent test failed: {result['error']}")
    
    return result


# Include authentication test endpoints from main.py
@app.get("/api/auth/me")
def get_current_user_info(user_id: str = Depends(get_current_user_id)):
    """
    Get current authenticated user information.
    """
    return {
        "user_id": user_id,
        "authenticated": True,
    }


@app.get("/api/protected")
def get_protected_resource(user_id: str = Depends(get_current_user_id)):
    """
    Example protected endpoint that requires authentication.
    """
    return {
        "message": "You have access to this protected resource",
        "user_id": user_id,
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting DEBUG_API server on http://localhost:8000")
    logger.info(f"Provider: {'OpenRouter' if is_openrouter else 'OpenAI'}")
    logger.info(f"Base URL: {settings.OPENAI_BASE_URL}")
    logger.info(f"Model: {settings.OPENAI_AGENT_MODEL}")
    logger.info("Available debug endpoints:")
    logger.info("  - GET /debug/config")
    logger.info("  - GET /debug/test-db")
    logger.info("  - GET /debug/test-openai")
    logger.info("  - GET /debug/test-agent")
    logger.info("  - GET /health")
    logger.info("=" * 80)
    
    uvicorn.run(
        "debug_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
