# Phase III Implementation Plan: Todo AI Chatbot

**Version**: 1.0.0  
**Created**: 2026-03-05  
**Based On**: `/specs/todo-ai-spec.md`  
**Methodology**: Agentic Dev Stack (Spec → Plan → Task → Implement)

---

## Overview

This implementation plan breaks down Phase III into **6 phases** with **47 atomic tasks**. Each task is designed to be:
- ✅ **Atomic** - Single, focused implementation unit
- ✅ **Testable** - Can be verified independently
- ✅ **Trackable** - Clear completion criteria

---

## Phase 3.1: Backend Foundation & Dependencies

**Goal**: Set up the FastAPI backend structure with all required dependencies for Phase III.

### Tasks

- [ ] **3.1.1** - Update `backend/requirements.txt` with Phase III dependencies:
  - `openai-agents>=0.0.1`
  - `mcp>=1.0.0`
  - `websockets>=12.0`
  - `pydantic>=2.0.0` (if not already present)

- [ ] **3.1.2** - Run `pip install -r requirements.txt` to install new dependencies

- [ ] **3.1.3** - Create directory structure for Phase III:
  - `backend/api/routers/chat.py`
  - `backend/mcp/`
  - `backend/mcp/tools/`
  - `backend/agents/`

- [ ] **3.1.4** - Update `.env` file with Phase III environment variables:
  - `OPENAI_API_KEY=sk-...`
  - `OPENAI_AGENT_MODEL=gpt-4o`
  - `CHATKIT_MAX_MESSAGES=50`

- [ ] **3.1.5** - Create `backend/config.py` for centralized configuration loading:
  - Load `OPENAI_API_KEY` from environment
  - Load `OPENAI_AGENT_MODEL` from environment
  - Load `DATABASE_URL` from environment
  - Load `BETTER_AUTH_SECRET` from environment

- [ ] **3.1.6** - Verify database connectivity by running a test query against Neon PostgreSQL

---

## Phase 3.2: Database Models (Conversation & Message)

**Goal**: Extend the existing SQLModel schema with Conversation and Message models for chat history.

### Tasks

- [ ] **3.2.1** - Open `backend/models.py` and review existing Task models

- [ ] **3.2.2** - Add `ConversationBase` SQLModel class:
  - `user_id: str` (indexed, required)
  - `session_id: str` (unique, indexed, required)

- [ ] **3.2.3** - Add `Conversation` table class extending `ConversationBase`:
  - `id: uuid.UUID` (primary key, auto-generated)
  - `created_at: datetime` (auto-generated)
  - `updated_at: datetime` (auto-generated)
  - Relationship to `Message` (one-to-many)

- [ ] **3.2.4** - Add `MessageBase` SQLModel class:
  - `role: str` (required: 'user', 'assistant', or 'system')
  - `content: str` (required)

- [ ] **3.2.5** - Add `Message` table class extending `MessageBase`:
  - `id: uuid.UUID` (primary key, auto-generated)
  - `conversation_id: uuid.UUID` (foreign key to Conversation)
  - `created_at: datetime` (auto-generated)
  - Relationship to `Conversation` (many-to-one)

- [ ] **3.2.6** - Add `MessageRead` schema class for API responses:
  - Include: `id`, `conversation_id`, `role`, `content`, `created_at`

- [ ] **3.2.7** - Add `ConversationRead` schema class for API responses:
  - Include: `id`, `user_id`, `session_id`, `created_at`, `updated_at`

- [ ] **3.2.8** - Update `backend/database.py` to export `init_db()` function for table creation

- [ ] **3.2.9** - Run database migrations to create `conversation` and `message` tables in Neon PostgreSQL

- [ ] **3.2.10** - Create unit tests for Conversation and Message model instantiation

---

## Phase 3.3: Authentication Middleware

**Goal**: Implement JWT authentication middleware to extract `user_id` for all chat operations.

### Tasks

- [ ] **3.3.1** - Review existing `backend/security.py` for JWT validation logic

- [ ] **3.3.2** - Create `backend/middleware/auth.py` with FastAPI dependency:
  - Function `get_current_user(authorization: str)` 
  - Extract JWT from `Authorization: Bearer <token>` header
  - Validate token signature using `BETTER_AUTH_SECRET`
  - Return `user_id` from decoded token

- [ ] **3.3.3** - Handle authentication errors:
  - Return `401 Unauthorized` for missing token
  - Return `401 Unauthorized` for invalid/expired token

- [ ] **3.3.4** - Create `backend/middleware/__init__.py` to export auth dependency

- [ ] **3.3.5** - Write unit tests for auth middleware:
  - Test valid JWT token
  - Test missing token
  - Test expired token
  - Test invalid signature

---

## Phase 3.4: MCP Tools Implementation

**Goal**: Implement all 5 MCP tools with automatic `user_id` injection and security validation.

### Tasks

- [ ] **3.4.1** - Create `backend/mcp/__init__.py` with MCP server initialization:
  - Import `tool` decorator from `mcp` package
  - Create MCP server instance

- [ ] **3.4.2** - Create `backend/mcp/context.py` with MCP Context class:
  - Store `user_id` in context metadata
  - Provide access to session information

- [ ] **3.4.3** - Implement `add_task` MCP tool in `backend/mcp/tools/add_task.py`:
  - Parameters: `title: str`, `description: str = None`
  - Extract `user_id` from context
  - Create Task with SQLModel session
  - Return created task as dict

- [ ] **3.4.4** - Implement `list_tasks` MCP tool in `backend/mcp/tools/list_tasks.py`:
  - Parameters: `completed: bool = None`
  - Extract `user_id` from context
  - Query tasks filtered by `user_id`
  - Return `{tasks: [...], count: int}`

- [ ] **3.4.5** - Implement `complete_task` MCP tool in `backend/mcp/tools/complete_task.py`:
  - Parameters: `task_id: uuid.UUID`
  - Extract `user_id` from context
  - Query task by `task_id` AND `user_id` (security)
  - Set `completed = True`
  - Return updated task

- [ ] **3.4.6** - Implement `delete_task` MCP tool in `backend/mcp/tools/delete_task.py`:
  - Parameters: `task_id: uuid.UUID`
  - Extract `user_id` from context
  - Query task by `task_id` AND `user_id` (security)
  - Delete task from session
  - Return `{success: bool, deleted_id: uuid}`

- [ ] **3.4.7** - Implement `update_task` MCP tool in `backend/mcp/tools/update_task.py`:
  - Parameters: `task_id: uuid.UUID`, `title: str = None`, `description: str = None`, `completed: bool = None`
  - Extract `user_id` from context
  - Query task by `task_id` AND `user_id` (security)
  - Update provided fields
  - Return updated task

- [ ] **3.4.8** - Create `backend/mcp/tools/__init__.py` to export all tools

- [ ] **3.4.9** - Implement security wrapper for all MCP tools:
  - Validate `user_id` exists before any operation
  - Return `401 Unauthorized` if missing

- [ ] **3.4.10** - Write unit tests for each MCP tool:
  - Test successful operation
  - Test missing `user_id`
  - Test task not found (returns generic error for security)
  - Test cross-user access attempt (should fail silently)

---

## Phase 3.5: OpenAI Agent Integration

**Goal**: Configure OpenAI Agents SDK with MCP tools and system instructions.

### Tasks

- [ ] **3.5.1** - Create `backend/agents/instructions.py` with agent system prompt:
  - Define task management persona
  - List available tools and their purposes
  - Include security constraints
  - Include conversational guidelines

- [ ] **3.5.2** - Create `backend/agents/task_agent.py` with OpenAI Agent configuration:
  - Initialize agent with `OPENAI_AGENT_MODEL`
  - Attach all 5 MCP tools
  - Set system instructions from `instructions.py`

- [ ] **3.5.3** - Create `backend/agents/__init__.py` to export agent instance

- [ ] **3.5.4** - Implement agent message processing function:
  - Accept: `session_id`, `user_message`, `user_id`
  - Load conversation history (last 50 messages)
  - Send to OpenAI Agent
  - Process tool calls
  - Return agent response

- [ ] **3.5.5** - Implement tool call execution handler:
  - Parse tool name and arguments from agent response
  - Execute corresponding MCP tool
  - Capture tool execution result
  - Return result to agent for response generation

- [ ] **3.5.6** - Implement error handling for agent failures:
  - Catch OpenAI API errors
  - Return user-friendly error messages
  - Log errors for debugging

- [ ] **3.5.7** - Write unit tests for agent integration:
  - Test agent initialization
  - Test message processing
  - Test tool call execution
  - Test error handling

---

## Phase 3.6: Chat API Endpoints

**Goal**: Implement REST API endpoints for chat session and message management.

### Tasks

- [ ] **3.6.1** - Create `backend/api/routers/chat.py` with FastAPI router

- [ ] **3.6.2** - Implement `POST /api/v1/chat/sessions` endpoint:
  - Require authentication (extract `user_id`)
  - Generate unique `session_id` (UUID)
  - Create Conversation record in database
  - Return `{session_id, created_at}`

- [ ] **3.6.3** - Implement `GET /api/v1/chat/sessions/{session_id}/messages` endpoint:
  - Require authentication
  - Verify session belongs to authenticated user
  - Query messages for conversation (ordered by `created_at`)
  - Limit to last 50 messages
  - Return `{messages: [...]}`

- [ ] **3.6.4** - Implement `POST /api/v1/chat/sessions/{session_id}/messages` endpoint:
  - Require authentication
  - Verify session belongs to authenticated user
  - Save user message to database
  - Call OpenAI Agent for processing
  - Execute any tool calls
  - Save assistant response to database
  - Return `{message, tool_calls}`

- [ ] **3.6.5** - Implement `DELETE /api/v1/chat/sessions/{session_id}` endpoint:
  - Require authentication
  - Verify session belongs to authenticated user
  - Delete conversation and all related messages (cascade)
  - Return `{success: true, deleted_session_id}`

- [ ] **3.6.6** - Implement `GET /mcp/manifest` endpoint:
  - Return MCP server manifest
  - Include all 5 tools with descriptions and schemas

- [ ] **3.6.7** - Update `backend/main.py` to include chat router:
  - `app.include_router(chat.router, prefix="/api/v1/chat")`
  - `app.include_router(mcp_router, prefix="/mcp")`

- [ ] **3.6.8** - Add CORS configuration for chat endpoints (if not already global)

- [ ] **3.6.9** - Implement request/response logging middleware for chat endpoints

- [ ] **3.6.10** - Write integration tests for all chat endpoints:
  - Test session creation
  - Test message retrieval
  - Test message sending (with and without tool calls)
  - Test session deletion
  - Test authentication failures
  - Test cross-user session access (should fail)

---

## Phase 3.7: Conversation History Management

**Goal**: Implement stateless conversation history storage and retrieval for context-aware AI responses.

### Tasks

- [ ] **3.7.1** - Create `backend/services/conversation_service.py`

- [ ] **3.7.2** - Implement `create_conversation(user_id: str)` function:
  - Generate UUID `session_id`
  - Create Conversation record
  - Return conversation object

- [ ] **3.7.3** - Implement `get_conversation(session_id: str, user_id: str)` function:
  - Query conversation by `session_id` AND `user_id`
  - Return conversation or None

- [ ] **3.7.4** - Implement `get_messages(session_id: str, limit: int = 50)` function:
  - Query messages by conversation
  - Order by `created_at` ascending
  - Limit to last N messages
  - Return list of messages

- [ ] **3.7.5** - Implement `add_message(conversation_id: uuid.UUID, role: str, content: str)` function:
  - Create Message record
  - Return created message

- [ ] **3.7.6** - Implement `delete_conversation(session_id: str, user_id: str)` function:
  - Delete conversation (messages cascade delete via foreign key)
  - Return success boolean

- [ ] **3.7.7** - Implement `build_context_messages(messages: list)` function:
  - Format messages for OpenAI Agent input
  - Convert to `{role, content}` format
  - Handle truncation if exceeds token limit

- [ ] **3.7.8** - Write unit tests for all conversation service functions

---

## Phase 3.8: Frontend Integration (OpenAI ChatKit)

**Goal**: Integrate OpenAI ChatKit with the FastAPI backend for the chat UI.

### Tasks

- [ ] **3.8.1** - Navigate to `frontend/` directory

- [ ] **3.8.2** - Install OpenAI ChatKit: `npm install @openai/chatkit`

- [ ] **3.8.3** - Create `frontend/components/ChatInterface.tsx`:
  - Import `ChatKitProvider` and `ChatWidget`
  - Configure API endpoints
  - Integrate with Better Auth provider

- [ ] **3.8.4** - Create `frontend/lib/chatkit-config.ts`:
  - Define `apiUrl = "http://localhost:8000/api/v1/chat"`
  - Define `sessionEndpoint = "/sessions"`
  - Define `messagesEndpoint = "/messages"`
  - Configure auth token injection

- [ ] **3.8.5** - Create chat page `frontend/app/chat/page.tsx` (or equivalent route)

- [ ] **3.8.6** - Add chat navigation to existing frontend (add link/button to access chat)

- [ ] **3.8.7** - Test chat interface with backend:
  - Create new session
  - Send messages
  - Verify AI responses
  - Verify task operations execute correctly

- [ ] **3.8.8** - Style chat interface to match existing Phase II UI design

---

## Phase 3.9: Testing & Quality Assurance

**Goal**: Comprehensive testing of all Phase III functionality.

### Tasks

- [ ] **3.9.1** - Run all unit tests for MCP tools

- [ ] **3.9.2** - Run all unit tests for conversation service

- [ ] **3.9.3** - Run all integration tests for chat API endpoints

- [ ] **3.9.4** - Test end-to-end conversation flow:
  - User creates session
  - User sends "Add a task to buy groceries"
  - Verify task created in database
  - Verify AI response returned
  - Verify messages stored in database

- [ ] **3.9.5** - Test multi-tenant isolation:
  - Create two test users
  - Have each user create tasks via AI
  - Verify User A cannot see User B's tasks
  - Verify User A cannot modify User B's tasks

- [ ] **3.9.6** - Test ambiguous language handling:
  - Send "Do that thing" to AI
  - Verify AI asks clarifying question

- [ ] **3.9.7** - Test error scenarios:
  - Send message with expired token
  - Send message with invalid session_id
  - Request non-existent task
  - Verify appropriate error responses

- [ ] **3.9.8** - Performance test:
  - Measure average response time (target: < 3 seconds)
  - Test with concurrent users

- [ ] **3.9.9** - Verify backward compatibility:
  - Test all Phase II API endpoints still work
  - Verify no breaking changes

- [ ] **3.9.10** - Document any known issues or limitations

---

## Phase 3.10: Deployment & Documentation

**Goal**: Prepare Phase III for production deployment.

### Tasks

- [ ] **3.10.1** - Update `backend/README.md` with Phase III setup instructions

- [ ] **3.10.2** - Document all environment variables required

- [ ] **3.10.3** - Create deployment checklist

- [ ] **3.10.4** - Update root `README.md` with Phase III features

- [ ] **3.10.5** - Create API documentation (OpenAPI/Swagger if not auto-generated)

- [ ] **3.10.6** - Verify production database migrations are ready

- [ ] **3.10.7** - Test deployment to staging environment

- [ ] **3.10.8** - Conduct final user acceptance testing (UAT)

---

## Summary

| Phase | Description | Tasks | Status |
|-------|-------------|-------|--------|
| 3.1 | Backend Foundation | 6 | ⏳ Pending |
| 3.2 | Database Models | 10 | ⏳ Pending |
| 3.3 | Auth Middleware | 5 | ⏳ Pending |
| 3.4 | MCP Tools | 10 | ⏳ Pending |
| 3.5 | OpenAI Agent | 7 | ⏳ Pending |
| 3.6 | Chat API | 10 | ⏳ Pending |
| 3.7 | Conversation Service | 8 | ⏳ Pending |
| 3.8 | Frontend Integration | 8 | ⏳ Pending |
| 3.9 | Testing & QA | 10 | ⏳ Pending |
| 3.10 | Deployment | 8 | ⏳ Pending |
| **Total** | | **82 tasks** | |

---

## Task Dependencies

```
3.1 (Foundation) ─────────────────┬─────────────┐
                                  │             │
                                  ▼             ▼
3.2 (Database Models)         3.3 (Auth)        │
        │                         │             │
        ▼                         ▼             │
3.4 (MCP Tools) ◄─────────────────┘             │
        │                                       │
        ▼                                       │
3.5 (OpenAI Agent) ◄────────────────────────────┘
        │
        ▼
3.6 (Chat API) ◄───────────────────────────┐
        │                                   │
        ▼                                   │
3.7 (Conversation Service) ◄────────────────┘
        │
        ▼
3.8 (Frontend Integration)
        │
        ▼
3.9 (Testing & QA)
        │
        ▼
3.10 (Deployment)
```

---

## Next Steps

1. **Review** this plan with stakeholders
2. **Prioritize** phases based on MVP requirements
3. **Begin** with Phase 3.1 (Backend Foundation)
4. **Track** progress by checking off completed tasks
5. **Update** this document as implementation evolves
