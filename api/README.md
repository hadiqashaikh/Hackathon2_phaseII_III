# Todo AI Chatbot API

FastAPI backend for Todo AI Chatbot with OpenRouter integration.

## Quick Start

### 1. Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file in the `api` folder:

```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key
OPENROUTER_API_KEY=sk-or-v1-your-api-key
DEBUG=True
```

### 3. Run the Server

```bash
# Using start.bat (Windows)
start.bat

# Or manually
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Root:** http://localhost:8000/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/{id}` | Get a task |
| PUT | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |
| POST | `/api/chat/message` | Send chat message |
| GET | `/api/chat/conversations` | List conversations |
| DELETE | `/api/chat/conversations/{id}` | Delete conversation |

## Project Structure

```
api/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration & env vars
├── database.py          # Database connection
├── models.py            # SQLModel definitions
├── routers/             # API route handlers
│   ├── tasks.py         # Task CRUD operations
│   ├── chat.py          # Chat endpoint
│   └── quick_tasks.py   # Direct task operations
├── middleware/          # Auth & middleware
│   └── auth.py          # JWT authentication
├── ai_agents/           # AI agent logic
│   └── openrouter_agent.py
├── mcp_server/          # MCP tools
│   ├── context.py
│   └── tools/
│       └── task_tools.py
└── requirements.txt     # Python dependencies
```

## Vercel Deployment

This API is configured for Vercel deployment. The root `vercel.json` routes:
- `/api/*` → `api/main.py` (FastAPI)
- `/*` → `my-todo/` (Frontend)

### Vercel Build Settings

- **Root Directory:** *(leave empty)*
- **Build Command:** `cd my-todo && npm run build`
- **Output Directory:** `my-todo/dist`
