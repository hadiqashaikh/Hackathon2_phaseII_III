"""
Database configuration using SQLModel with Neon PostgreSQL.
"""

from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for database session."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_session_direct() -> Session:
    """Get session directly (for tools)."""
    return Session(engine)
