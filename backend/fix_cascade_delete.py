"""
Fix foreign key constraint to enable CASCADE delete.
This will allow deleting conversations without manually deleting messages first.
"""

from sqlalchemy import text
from database import engine

def fix_cascade_delete():
    """Add ON DELETE CASCADE to message table foreign key."""
    
    with engine.connect() as conn:
        try:
            # Drop existing foreign key constraint
            print("Dropping existing foreign key constraint...")
            conn.execute(text("""
                ALTER TABLE message 
                DROP CONSTRAINT IF EXISTS message_conversation_id_fkey;
            """))
            conn.commit()
            
            # Recreate with ON DELETE CASCADE
            print("Creating new foreign key with CASCADE delete...")
            conn.execute(text("""
                ALTER TABLE message
                ADD CONSTRAINT message_conversation_id_fkey
                FOREIGN KEY (conversation_id)
                REFERENCES conversation(id)
                ON DELETE CASCADE;
            """))
            conn.commit()
            
            print("✓ Successfully fixed foreign key constraint!")
            print("✓ Now deleting a conversation will automatically delete its messages.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    fix_cascade_delete()
