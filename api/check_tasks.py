"""Check tasks in database."""
from sqlmodel import Session, select
from models import Task
from database import get_session_direct

s = get_session_direct()
tasks = s.exec(select(Task).where(Task.user_id == 'debug-user')).all()
print(f'Tasks found: {len(tasks)}')
for t in tasks:
    print(f'  - {t.title} (completed: {t.completed})')
s.close()
