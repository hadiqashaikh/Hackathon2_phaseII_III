"""
Initialize Database - Create all tables for Better Auth and App
Run this once to set up the database.
"""

import sys
sys.path.insert(0, '.')

from database import engine, init_db
from sqlmodel import SQLModel, Session, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_better_auth_tables():
    """Create Better Auth required tables."""
    logger.info("Creating Better Auth tables...")
    
    with Session(engine) as session:
        # Create user table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "user" (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                "emailVerified" BOOLEAN NOT NULL DEFAULT false,
                image TEXT,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        
        # Create session table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "session" (
                id TEXT PRIMARY KEY,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                "expiresAt" TIMESTAMP NOT NULL,
                token TEXT NOT NULL UNIQUE,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "ipAddress" TEXT,
                "userAgent" TEXT
            )
        """))
        
        # Create account table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "account" (
                id TEXT PRIMARY KEY,
                "accountId" TEXT NOT NULL,
                "providerId" TEXT NOT NULL,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                "accessToken" TEXT,
                "refreshToken" TEXT,
                "idToken" TEXT,
                "accessTokenExpiresAt" TIMESTAMP,
                "refreshTokenExpiresAt" TIMESTAMP,
                scope TEXT,
                password TEXT,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        
        # Create verification table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "verification" (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                value TEXT NOT NULL,
                "expiresAt" TIMESTAMP NOT NULL,
                "createdAt" TIMESTAMP DEFAULT NOW(),
                "updatedAt" TIMESTAMP DEFAULT NOW()
            )
        """))
        
        session.commit()
        logger.info("✓ Better Auth tables created successfully")


def create_app_tables():
    """Create application tables (tasks, conversations, messages)."""
    logger.info("Creating application tables...")
    
    with Session(engine) as session:
        # Create task table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "task" (
                id TEXT PRIMARY KEY,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT false,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        
        # Create conversation table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "conversation" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                session_id TEXT NOT NULL UNIQUE,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
                "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        
        # Create message table
        session.exec(text("""
            CREATE TABLE IF NOT EXISTS "message" (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                "conversationId" UUID NOT NULL REFERENCES "conversation"(id) ON DELETE CASCADE,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                "createdAt" TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        
        session.commit()
        logger.info("✓ Application tables created successfully")


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Database Initialization")
    logger.info("=" * 50)
    
    try:
        # Create all tables
        create_better_auth_tables()
        create_app_tables()
        
        logger.info("=" * 50)
        logger.info("✓ Database initialization complete!")
        logger.info("=" * 50)
        logger.info("You can now start the backend with: uvicorn main:app --reload --port 8000")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
