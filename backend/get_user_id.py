"""
Quick script to get a valid user ID from the database.
"""

from sqlmodel import Session, select, text
from database import engine

# Simple query to get first user
with Session(engine) as session:
    result = session.exec(text('SELECT id FROM "user" LIMIT 1'))
    user_id = result.first()
    if user_id:
        print(f"Found user ID: {user_id}")
    else:
        print("No users found in database")
