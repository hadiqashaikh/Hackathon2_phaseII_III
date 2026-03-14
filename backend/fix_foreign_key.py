"""
Fix the foreign key constraint on the task table.
This removes the FK constraint so tasks can be created without a user record.
"""

from sqlalchemy import text
from database import get_session_direct

session = get_session_direct()

try:
    print("Checking for foreign key constraint on task table...")
    
    # Find the constraint name
    constraints = session.exec(text("""
        SELECT conname
        FROM pg_constraint
        WHERE conrelid = 'task'::regclass
        AND contype = 'f'
    """)).all()
    
    print(f"Found constraints: {constraints}")
    
    # Drop the foreign key constraint
    for constraint in constraints:
        constraint_name = constraint[0]
        if 'userid' in constraint_name.lower() or 'user' in constraint_name.lower():
            print(f"Dropping constraint: {constraint_name}")
            session.exec(text(f'ALTER TABLE task DROP CONSTRAINT IF EXISTS {constraint_name}'))
            session.commit()
            print(f"✅ Dropped constraint: {constraint_name}")
    
    print("\n✅ Foreign key constraint removed!")
    print("You can now create tasks without a user record.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    session.rollback()
    import traceback
    traceback.print_exc()
finally:
    session.close()
