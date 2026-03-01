import logging
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from models import Task
from database import get_session
from jose import JWTError, jwt
from datetime import datetime
from dotenv import load_dotenv
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

ALGORITHM = "HS256"

def verify_token(token: str) -> dict:
    """Verify JWT token and extract user information."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            logger.warning("Token does not contain user ID")
            raise credentials_exception
    except JWTError as e:
        logger.warning(f"JWT token validation failed: {str(e)}")
        raise credentials_exception

    # Check if token is expired
    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
        logger.warning("Token is expired")
        raise credentials_exception

    logger.info(f"Successfully validated token for user_id: {user_id}")
    return payload

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token."""
    return verify_token(credentials.credentials)

def verify_user_owns_task(user_id: str, task: Task) -> None:
    """Verify that the user owns the task."""
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )