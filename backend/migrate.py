"""
Database Migration Script for Phase III: Todo AI Chatbot.

This script initializes the database by creating all tables defined in models.py.
It is safe to run multiple times - it will only create tables that don't exist.

Usage:
    python migrate.py

Or import the function:
    from database import init_db
    init_db()
"""

import sys
from sqlmodel import SQLModel, text
from database import engine, init_db
from models import Task, Conversation, Message  # Import all models to ensure registration


def check_connection() -> bool:
    """Test database connection."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[OK] Database connection successful")
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False


def list_existing_tables() -> list:
    """List existing tables in the database."""
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables


def migrate() -> None:
    """
    Run database migrations to create all tables.
    
    This function:
    1. Tests the database connection
    2. Lists existing tables
    3. Creates any missing tables
    4. Reports the final state
    """
    print("=" * 60)
    print("Phase III: Database Migration")
    print("=" * 60)
    
    # Step 1: Check connection
    print("\n[1/4] Checking database connection...")
    if not check_connection():
        print("\n[ERROR] Migration aborted: Cannot connect to database")
        sys.exit(1)
    
    # Step 2: List existing tables
    print("\n[2/4] Checking existing tables...")
    existing_tables = list_existing_tables()
    if existing_tables:
        print(f"    Existing tables: {', '.join(existing_tables)}")
    else:
        print("    No existing tables found")
    
    # Step 3: Create tables
    print("\n[3/4] Creating tables (if not exists)...")
    init_db()
    print("    [OK] Tables created successfully")
    
    # Step 4: Verify final state
    print("\n[4/4] Verifying final state...")
    final_tables = list_existing_tables()
    print(f"    Final tables: {', '.join(final_tables)}")
    
    # Verify Phase III tables exist
    required_tables = {"task", "conversation", "message"}
    created_tables = required_tables.intersection(set(final_tables))
    missing_tables = required_tables - set(final_tables)
    
    print("\n" + "=" * 60)
    if not missing_tables:
        print("[SUCCESS] Migration completed successfully!")
        print(f"    All {len(created_tables)} required tables are present:")
        for table in sorted(created_tables):
            print(f"      - {table}")
    else:
        print("[WARNING] Migration completed with warnings")
        print(f"    Missing tables: {', '.join(missing_tables)}")
        print("    Please check the models and try again.")
    print("=" * 60)


if __name__ == "__main__":
    migrate()
