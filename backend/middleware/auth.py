"""
Authentication Middleware for Phase III: Todo AI Chatbot.

This module provides FastAPI dependencies for validating Better Auth sessions
by checking the database directly (not JWT decoding).

Better Auth uses opaque session IDs stored in the database, not standard JWTs.

DEBUG MODE: If DEBUG=True in .env, will fallback to last active user if session check fails.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os

from config import settings
from database import get_session_direct
from sqlalchemy import text

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# DEBUG MODE - Check if enabled
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
if DEBUG_MODE:
    logger.warning("=" * 60)
    logger.warning("DEBUG MODE ENABLED - Will fallback to last active user")
    logger.warning("=" * 60)

# HTTP Bearer token security scheme (for fallback)
security = HTTPBearer(auto_error=False)


class AuthError(HTTPException):
    """Custom exception for authentication errors."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_session_token(token: str) -> Optional[dict]:
    """
    Verify session token by checking the database.

    Better Auth stores sessions in the 'session' table with:
    - id: session token
    - userId: reference to user
    - expires: expiration timestamp

    Tries multiple table name variations: session, "session", Session

    Args:
        token: Session token string from cookie or Authorization header

    Returns:
        User info dict with 'id' and 'userId' if valid, None if invalid/expired
    """
    session = None
    try:
        logger.debug(f"Verifying session token in database (length: {len(token)})")
        logger.debug(f"Token preview: {token[:20]}..." if len(token) > 20 else f"Token: {token}")
        session = get_session_direct()

        # Try multiple table name variations
        table_names_to_try = ['"session"', 'session', '"Session"', 'Session']
        result = None
        
        for table_name in table_names_to_try:
            try:
                # Query the session table to find valid session
                query = text(f"""
                    SELECT id, "userId", expires
                    FROM {table_name}
                    WHERE id = :token
                    AND (expires IS NULL OR expires > NOW())
                    LIMIT 1
                """)
                
                result = session.exec(query, {"token": token}).first()
                if result:
                    logger.info(f"Found session in table: {table_name}")
                    break
                else:
                    logger.debug(f"No session found in table: {table_name}")
            except Exception as table_error:
                logger.debug(f"Table {table_name} query failed: {type(table_error).__name__}")
                continue
        
        if result:
            user_id = result[1]  # userId column
            logger.info(f"✓ Session validated for userId: {user_id}")
            return {
                "id": user_id,
                "userId": user_id,
                "sub": user_id,
            }
        else:
            logger.warning("⚠ Session not found in database or expired")
            
            # Check if session exists but is expired
            for table_name in table_names_to_try:
                try:
                    expired_check = session.exec(text(f"""
                        SELECT id, "userId", expires
                        FROM {table_name}
                        WHERE id = :token
                        LIMIT 1
                    """), {"token": token}).first()
                    
                    if expired_check:
                        logger.warning(f"Session found but expired at: {expired_check[2]}")
                        break
                except:
                    continue
            
            # DEBUG MODE: Fallback to last active user
            if DEBUG_MODE:
                logger.warning("DEBUG MODE: Attempting fallback to last active user...")
                try:
                    # Try to get the last active user from the user table
                    user_table_names = ['"user"', 'user', '"User"', 'User']
                    for user_table in user_table_names:
                        try:
                            last_user = session.exec(text(f"""
                                SELECT id, email, name
                                FROM {user_table}
                                ORDER BY "createdAt" DESC
                                LIMIT 1
                            """)).first()
                            
                            if last_user:
                                logger.warning(f"DEBUG MODE: Using fallback user: {last_user[0]} ({last_user[1]})")
                                return {
                                    "id": last_user[0],
                                    "userId": last_user[0],
                                    "sub": last_user[0],
                                    "email": last_user[1],
                                    "debug_mode": True,
                                }
                        except:
                            continue
                except Exception as fallback_error:
                    logger.error(f"DEBUG MODE fallback failed: {fallback_error}")
            
            return None

    except Exception as e:
        logger.error(f"Database error during session validation: {type(e).__name__}: {str(e)}")
        logger.error(f"Full traceback available in debug logs")
        
        # DEBUG MODE: Emergency fallback
        if DEBUG_MODE:
            logger.warning("DEBUG MODE: Database error - attempting emergency fallback")
            return {
                "id": "debug-user",
                "userId": "debug-user",
                "sub": "debug-user",
                "debug_mode": True,
                "error": str(e),
            }
        
        return None
    finally:
        if session:
            session.close()


def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extract session token from cookie.

    Better Auth stores the session token in various cookie names depending on configuration.
    This function handles both raw tokens and prefixed ones.

    Args:
        request: FastAPI request object

    Returns:
        Token string if found, None otherwise
    """
    logger.debug(f"Checking cookies for session token...")
    logger.debug(f"Available cookie names: {list(request.cookies.keys())}")
    
    # Log all cookies with their lengths for debugging
    for cookie_name, cookie_value in request.cookies.items():
        logger.debug(f"  Cookie '{cookie_name}': {len(cookie_value) if cookie_value else 0} chars")

    # Comprehensive list of cookie names used by Better Auth
    cookie_names = [
        # Standard Better Auth cookie names
        "better-auth.session_token",
        "better-auth.session-token",
        "better-auth_token",
        "better-auth-token",
        # Common variations
        "session_token",
        "session-token",
        "auth_token",
        "auth-token",
        # Legacy/alternative names
        "better_auth",
        "auth",
        "session",
        "token",
    ]

    for cookie_name in cookie_names:
        token = request.cookies.get(cookie_name)
        if token:
            # Handle prefixed tokens (some setups add prefixes)
            clean_token = token
            if token.startswith("j:"):
                logger.debug("Removing 'j:' prefix from token")
                clean_token = token[2:]
            elif token.startswith("u:"):
                logger.debug("Removing 'u:' prefix from token")
                clean_token = token[2:]
            
            logger.info(f"✓ Found session token in cookie: {cookie_name} (length: {len(clean_token)})")
            return clean_token

    # Also check for cookies starting with 'better-auth' or 'better_auth'
    for cookie_name, cookie_value in request.cookies.items():
        logger.debug(f"Checking cookie: {cookie_name} (length: {len(cookie_value) if cookie_value else 0})")
        if cookie_name.startswith('better-auth') or cookie_name.startswith('better_auth'):
            if cookie_value and len(cookie_value) > 10:  # Likely a token
                # Clean the token
                clean_token = cookie_value
                if cookie_value.startswith("j:") or cookie_value.startswith("u:"):
                    clean_token = cookie_value[2:]
                
                logger.info(f"✓ Found session token in cookie: {cookie_name}")
                return clean_token

    logger.warning("⚠ No session token found in cookies")
    return None


async def get_current_user_id(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    FastAPI dependency that extracts and validates user_id from request.

    Supports both:
    1. Session cookie (Better Auth default) - validated against database
    2. Authorization: Bearer <token> header - validated against database

    Args:
        request: FastAPI request object
        credentials: Optional Bearer token from Authorization header

    Returns:
        user_id (str) extracted from validated session

    Raises:
        AuthError: If authentication fails
    """
    token = None

    # Priority 1: Check cookies (Better Auth default)
    token = get_token_from_cookie(request)

    # Priority 2: Check Authorization header
    if not token and credentials:
        token = credentials.credentials
        logger.debug("Using token from Authorization header")

    # No token found
    if not token:
        logger.warning("⚠ No authentication token found")
        raise AuthError(detail="Authentication required")

    # Verify session against database
    payload = verify_session_token(token)

    if not payload:
        logger.warning("⚠ Session validation failed")
        if DEBUG_MODE:
            logger.warning("DEBUG MODE: Allowing request despite validation failure")
            return "debug-user"
        raise AuthError(detail="Invalid or expired session")

    user_id = payload.get("id") or payload.get("userId") or payload.get("sub")

    if not user_id:
        logger.warning("⚠ Session does not contain user ID")
        raise AuthError(detail="Invalid session format")

    return user_id


async def get_current_user_payload(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> dict:
    """
    FastAPI dependency that returns the full user payload from session.

    Similar to get_current_user_id but returns the entire session payload.

    Args:
        request: FastAPI request object
        credentials: Optional Bearer token from Authorization header

    Returns:
        Full session payload (dict)

    Raises:
        AuthError: If authentication fails
    """
    token = None

    # Priority 1: Check cookies
    token = get_token_from_cookie(request)

    # Priority 2: Check Authorization header
    if not token and credentials:
        token = credentials.credentials
        logger.debug("Using token from Authorization header")

    # No token found
    if not token:
        logger.warning("⚠ No authentication token found")
        raise AuthError(detail="Authentication required")

    # Verify session against database
    payload = verify_session_token(token)

    if not payload:
        logger.warning("⚠ Session validation failed")
        if DEBUG_MODE:
            logger.warning("DEBUG MODE: Allowing request despite validation failure")
            return {"id": "debug-user", "userId": "debug-user", "debug_mode": True}
        raise AuthError(detail="Invalid or expired session")

    return payload


# Optional authentication dependency - allows unauthenticated requests
# but returns user_id if valid token is provided
async def get_optional_user_id(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[str]:
    """
    FastAPI dependency that optionally extracts user_id if token is present.

    Unlike get_current_user_id, this does NOT raise an error if no token is provided.
    Useful for public endpoints that can optionally use authentication.

    Args:
        request: FastAPI request object
        credentials: Optional Bearer token from Authorization header

    Returns:
        user_id (str) if valid token provided, None otherwise
    """
    token = None

    # Check cookies
    token = get_token_from_cookie(request)

    # Check Authorization header
    if not token and credentials:
        token = credentials.credentials

    # No token - return None (don't raise error)
    if not token:
        return None

    # Try to verify session against database
    payload = verify_session_token(token)

    if not payload:
        return None

    return payload.get("id") or payload.get("userId") or payload.get("sub")
