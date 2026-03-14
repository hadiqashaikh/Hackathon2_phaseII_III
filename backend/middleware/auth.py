"""
Authentication Middleware using Better Auth sessions.
Validates sessions against the database.
"""

import logging
from typing import Optional
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os

from config import settings
from database import get_session_direct
from sqlalchemy import text

load_dotenv()

logger = logging.getLogger(__name__)

# Debug mode
DEBUG_MODE = settings.DEBUG

security = HTTPBearer(auto_error=False)


class AuthError(HTTPException):
    """Authentication error exception."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_session_token(token: str) -> Optional[dict]:
    """
    Verify session token against database.
    Better Auth stores sessions in 'session' table.
    """
    session = None
    try:
        session = get_session_direct()

        # Try different table name variations
        for table_name in ['"session"', 'session']:
            try:
                result = session.exec(text(f"""
                    SELECT id, "userId"
                    FROM {table_name}
                    WHERE id = :token
                    AND ("expiresAt" IS NULL OR "expiresAt" > NOW())
                    LIMIT 1
                """), {"token": token}).first()

                if result:
                    user_id = result[1]
                    logger.debug(f"Session validated for userId: {user_id}")
                    return {"id": user_id, "userId": user_id, "sub": user_id}
            except Exception:
                continue

        # DEBUG MODE: Fallback to debug user
        if DEBUG_MODE:
            logger.warning("DEBUG MODE: Using fallback user")
            return {"id": "debug-user", "userId": "debug-user", "sub": "debug-user"}

        return None

    except Exception as e:
        logger.error(f"Session validation error: {e}")
        if DEBUG_MODE:
            return {"id": "debug-user", "userId": "debug-user", "sub": "debug-user"}
        return None

    finally:
        if session:
            session.close()


def get_token_from_cookie(request: Request) -> Optional[str]:
    """Extract session token from cookies."""
    cookie_names = [
        "better-auth.session_token",
        "better-auth.session-token",
        "session_token",
        "auth_token",
        "session",
    ]

    for cookie_name in cookie_names:
        token = request.cookies.get(cookie_name)
        if token:
            # Clean token if prefixed
            if token.startswith("j:") or token.startswith("u:"):
                token = token[2:]
            logger.debug(f"Found token in cookie: {cookie_name}")
            return token

    return None


async def get_current_user_id(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    FastAPI dependency to get authenticated user ID.
    Supports cookies and Bearer token.
    Falls back to debug-user if no valid session found.
    """
    token = None

    # Priority 1: Check cookies
    token = get_token_from_cookie(request)

    # Priority 2: Check Authorization header
    if not token and credentials:
        token = credentials.credentials

    # No token - use debug fallback
    if not token:
        logger.warning("No auth token found, using debug-user")
        return "debug-user"

    # Verify session
    payload = verify_session_token(token)

    if not payload:
        logger.warning("Invalid session, using debug-user")
        return "debug-user"

    user_id = payload.get("id") or payload.get("userId") or payload.get("sub")
    logger.info(f"Authenticated user_id: {user_id}")
    return user_id
