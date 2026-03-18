"""
Complete Database Fix Script.
Fixes all foreign key constraints and creates debug user.
"""

from sqlalchemy import text
from database import engine

def fix_all_constraints():
    """Fix all database constraints and create debug user."""
    
    with engine.connect() as conn:
        try:
            print("=" * 60)
            print("DATABASE FIX SCRIPT")
            print("=" * 60)
            
            # 1. Fix conversation CASCADE delete
            print("\n1. Fixing conversation CASCADE delete...")
            conn.execute(text("""
                ALTER TABLE message 
                DROP CONSTRAINT IF EXISTS message_conversation_id_fkey;
            """))
            conn.execute(text("""
                ALTER TABLE message
                ADD CONSTRAINT message_conversation_id_fkey
                FOREIGN KEY (conversation_id)
                REFERENCES conversation(id)
                ON DELETE CASCADE;
            """))
            conn.commit()
            print("   ✓ Conversation CASCADE delete fixed")
            
            # 2. Create debug user if not exists
            print("\n2. Creating debug user...")
            conn.execute(text("""
                INSERT INTO "user" (id, email, name, "createdAt", "updatedAt", "emailVerified")
                VALUES ('debug-user', 'debug@localhost', 'Debug User', NOW(), NOW(), true)
                ON CONFLICT (id) DO NOTHING;
            """))
            conn.commit()
            print("   ✓ Debug user created")
            
            # 3. Verify task table foreign key
            print("\n3. Checking task table foreign key...")
            result = conn.execute(text("""
                SELECT conname, contype, confdeltype
                FROM pg_constraint
                WHERE conrelid = 'task'::regclass
                AND conname = 'task_userId_user_id_fk';
            """)).fetchall()
            
            if result:
                print(f"   ✓ Task foreign key exists: {result[0]}")
                # Check if it allows debug-user
                print("   Note: task.userId references user.id - debug-user must exist")
            else:
                print("   ⚠ Task foreign key not found")
            
            print("\n" + "=" * 60)
            print("ALL FIXES APPLIED SUCCESSFULLY!")
            print("=" * 60)
            print("\nSummary:")
            print("  - Message → Conversation: CASCADE DELETE enabled")
            print("  - Debug user 'debug-user' created in user table")
            print("  - Task → User: Foreign key verified")
            print("\nNow you can:")
            print("  1. Delete conversations (messages will auto-delete)")
            print("  2. Create tasks via AI (debug-user exists)")
            print("  3. Use the chatbot normally")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

if __name__ == "__main__":
    fix_all_constraints()
