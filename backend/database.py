"""
Database configuration for Phase III: Todo AI Chatbot.

Uses SQLModel with Neon Serverless PostgreSQL.
"""

from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from config import settings

# Load database URL from centralized settings
DATABASE_URL = settings.DATABASE_URL

# Create engine with connection pooling for serverless PostgreSQL
engine = create_engine(
    DATABASE_URL,
    echo=settings.is_development,  # Enable SQL logging in development
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Max connections beyond pool_size
)


def init_db() -> None:
    """
    Initialize database by creating all tables.

    Call this on application startup to ensure all models are registered.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Usage:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            ...
    
    Note: This is a generator-based dependency for FastAPI.
    For direct usage, use get_session_direct() instead.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_session_direct() -> Session:
    """
    Get a database session directly (not as a generator).
    
    Use this for testing and direct session access.
    Remember to close the session when done.
    
    Usage:
        session = get_session_direct()
        try:
            session.exec(...)
        finally:
            session.close()
    """
    return Session(engine)
