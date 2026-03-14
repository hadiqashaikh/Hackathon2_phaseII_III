# Todo AI Chatbot Backend

FastAPI backend with AI-powered task management using OpenRouter (FREE tier).

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open docs
http://localhost:8000/docs
```

## Deployment

### Hugging Face Spaces

1. Create new Space with **Docker** SDK
2. Add environment variables in Settings:
   - `DATABASE_URL` - Your Neon PostgreSQL URL
   - `BETTER_AUTH_SECRET` - Random secret key
   - `OPENROUTER_API_KEY` - Get from openrouter.ai
   - `OPENROUTER_BASE_URL` - `https://openrouter.ai/api/v1`
   - `OPENROUTER_AGENT_MODEL` - `google/gemini-2.0-flash-lite-001`
3. Push code to Space
4. Wait for deployment (3-5 minutes)

### Environment Variables

```bash
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_AGENT_MODEL=google/gemini-2.0-flash-lite-001
DEBUG=True
```

## API Endpoints

### Tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/` - List tasks
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/toggle` - Toggle completion

### Chat (AI)
- `POST /api/chat/message` - Send message to AI
- `GET /api/chat/conversations` - List conversations
- `GET /api/chat/conversations/{id}` - Get conversation
- `DELETE /api/chat/conversations/{id}` - Delete conversation

### Quick Tasks
- `POST /api/quick-tasks/` - Create task directly
- `GET /api/quick-tasks/` - List tasks
- `DELETE /api/quick-tasks/{id}` - Delete task
- `PATCH /api/quick-tasks/{id}/toggle` - Toggle task

## Tech Stack

- **Framework**: FastAPI
- **Database**: Neon PostgreSQL (serverless)
- **ORM**: SQLModel
- **Auth**: Better Auth (JWT sessions)
- **AI**: OpenRouter (FREE tier - Gemini 2.0 Flash Lite)
- **Protocol**: MCP (Model Context Protocol)

## License

MIT
