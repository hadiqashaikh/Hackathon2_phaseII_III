"""
Create debug user in database for development.
"""

from sqlalchemy import text
from database import engine

def create_debug_user():
    """Create debug user in the user table."""
    
    with engine.connect() as conn:
        try:
            # Check if user table exists and create debug user
            print("Creating debug user...")
            
            # First check table structure
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'user'
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            print(f"User table columns: {columns}")
            
            # Try to insert debug user (adjust based on your schema)
            conn.execute(text("""
                INSERT INTO "user" (id, email, name, "createdAt")
                VALUES ('debug-user', 'debug@localhost', 'Debug User', NOW())
                ON CONFLICT (id) DO NOTHING;
            """))
            conn.commit()
            print("✓ Debug user created successfully!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
            
            # Try alternative schema
            try:
                print("Trying alternative schema...")
                conn.execute(text("""
                    INSERT INTO "user" (id, email)
                    VALUES ('debug-user', 'debug@localhost')
                    ON CONFLICT DO NOTHING;
                """))
                conn.commit()
                print("✓ Debug user created!")
            except Exception as e2:
                print(f"❌ Alternative also failed: {e2}")
                print("\nManual fix required:")
                print("1. Check your 'user' table schema")
                print("2. Run: INSERT INTO \"user\" (id, email) VALUES ('debug-user', 'debug@local');")

if __name__ == "__main__":
    create_debug_user()
