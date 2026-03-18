# Phase Two - Todo AI Chatbot

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      VERCEL / Production                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  /api/auth/*  →  Next.js API (Better Auth handler)          │
│  /api/*       →  FastAPI (Python backend)                   │
│  /*           →  Next.js (React frontend)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Local Development                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  localhost:3000  →  Next.js dev server                      │
│                      ↓ (proxies /api/* to localhost:8000)   │
│  localhost:8000  →  FastAPI backend                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start - Local Development

### 1. Start FastAPI Backend

```bash
cd api
python main.py
# Or with uvicorn:
# uvicorn main:app --reload --port 8000
```

Backend will run on: `http://localhost:8000`

### 2. Start Next.js Frontend

```bash
cd my-todo
npm run dev
```

Frontend will run on: `http://localhost:3000`

### 3. Open Browser

Navigate to: `http://localhost:3000`

## Environment Setup

### API (.env file)

Create `api/.env` with:

```env
DATABASE_URL="postgresql://user:password@localhost:5432/todo_db"
BETTER_AUTH_SECRET="your-secret-key-min-32-characters"
BETTER_AUTH_URL="http://localhost:3000"
OPENROUTER_API_KEY="sk-or-v1-your-api-key"
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
OPENROUTER_AGENT_MODEL="meta-llama/llama-3.2-3b-instruct:free"
CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
DEBUG="true"
```

### Frontend (.env.local file)

Create `my-todo/.env.local` with:

```env
DATABASE_URL="postgresql://user:password@localhost:5432/todo_db"
BETTER_AUTH_SECRET="your-secret-key-min-32-characters"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

## API Routes

### Authentication (Better Auth)
- `POST /api/auth/sign-up/email` - Create account
- `POST /api/auth/sign-in/email` - Sign in
- `POST /api/auth/sign-out` - Sign out
- `GET /api/auth/get-session` - Get current session

### Tasks (FastAPI)
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

### Chat (FastAPI)
- `POST /api/chat/message` - Send message to AI
- `GET /api/chat/conversations` - List conversations
- `GET /api/chat/conversations/{id}` - Get conversation
- `DELETE /api/chat/conversations/{id}` - Delete conversation

## Vercel Deployment

1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables in Vercel dashboard:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `BETTER_AUTH_URL` (your Vercel domain)
   - `OPENROUTER_API_KEY`
   - `CORS_ALLOWED_ORIGINS`
4. Deploy

## Troubleshooting

### Tasks not appearing after AI creates them

1. Check backend terminal for errors
2. Verify `DATABASE_URL` is same for both Next.js and FastAPI
3. Check browser console for CORS errors
4. Ensure cookies are being sent (check DevTools → Network)

### CORS Errors

1. Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `api/.env`
2. Ensure `allow_credentials=True` in CORS middleware
3. Check that cookies have correct `SameSite` attribute

### 404 on /api/* routes

1. Verify `vercel.json` is in project root
2. Check that `api/main.py` exists
3. For local dev, ensure Next.js proxy is configured in `next.config.ts`

### Auth Issues

1. Verify `BETTER_AUTH_SECRET` is same in both `.env` files
2. Check that session table exists in database
3. Enable `DEBUG="true"` for detailed logs

## Debug Mode

Set `DEBUG="true"` in `api/.env` to:
- Use fallback user when no session found
- See detailed SQL queries
- Get more verbose logging

## Database Schema

The app uses these tables:
- `user` - User accounts (Better Auth)
- `session` - User sessions (Better Auth)
- `account` - OAuth accounts (Better Auth)
- `verification` - Email verification tokens (Better Auth)
- `task` - Todo tasks
- `conversation` - Chat conversations
- `message` - Chat messages

All tables are auto-created on first run.
