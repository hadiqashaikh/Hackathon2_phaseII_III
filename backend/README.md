# FastAPI Task Backend

This is a Python backend service built with FastAPI that provides task management functionality with JWT-based authentication and user data isolation.

## Features

- JWT token authentication using Better Auth compatible tokens
- Secure task management with user data isolation
- Full CRUD operations for tasks
- Toggle task completion status
- Proper error handling and logging

## Prerequisites

- Python 3.10+
- PostgreSQL database (tested with Neon Serverless)
- Better Auth configured with JWT plugin on the frontend

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/db_name
BETTER_AUTH_SECRET=your_32_character_secret_key_here_must_be_at_least_32_characters
```

## Running the Application

```bash
uvicorn main:app --reload
```

The server will start on http://localhost:8000

## API Endpoints

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

### Create Task
```
POST /api/tasks/
```

### Get All Tasks
```
GET /api/tasks/
```

### Get Single Task
```
GET /api/tasks/{task_id}
```

### Update Task
```
PUT /api/tasks/{task_id}
```

### Delete Task
```
DELETE /api/tasks/{task_id}
```

### Toggle Task Completion
```
PATCH /api/tasks/{task_id}/toggle
```

## Architecture

- **main.py**: FastAPI application entry point
- **models.py**: SQLModel definitions for Task entity
- **database.py**: Database connection and session management
- **security.py**: JWT token validation and user extraction
- **api/routers/tasks.py**: Task CRUD endpoints with authentication
- **requirements.txt**: Python dependencies
- **.env**: Environment variables

## Security

- All endpoints require JWT authentication
- User data isolation through user_id filtering
- Proper validation of tokens (signature, expiration)
- Error responses don't reveal the existence of other users' data