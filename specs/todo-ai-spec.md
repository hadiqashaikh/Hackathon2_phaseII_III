# Technical Specification: Todo AI Chatbot (Phase III)

**Feature Branch**: `phase-iii-todo-ai-chatbot`  
**Created**: 2026-03-05  
**Status**: Draft  
**Version**: 1.0.0  
**Phase**: III (Builds upon Phase II - Next.js Todo App with Neon PostgreSQL)

---

## Executive Summary

This specification defines the architecture and implementation requirements for Phase III: Todo AI Chatbot. The system transforms the existing Phase II Next.js Todo application into an AI-powered task management experience using **FastAPI**, **OpenAI Agents SDK**, **Model Context Protocol (MCP)**, and **SQLModel** with the existing **Neon PostgreSQL** database.

The AI chatbot enables users to manage tasks through natural language conversations, leveraging 5 MCP tools for task operations while maintaining full compatibility with the existing Phase II authentication and data models.

---

## System Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend Framework | FastAPI (Python) | REST API and MCP server |
| AI Framework | OpenAI Agents SDK | Natural language processing and agent orchestration |
| Protocol | Model Context Protocol (MCP) | Standardized tool interface for AI agents |
| ORM | SQLModel | Database models and queries |
| Database | Neon Serverless PostgreSQL | Persistent storage (existing from Phase II) |
| Authentication | Better Auth | User authentication (existing from Phase II) |
| Frontend Chat UI | OpenAI ChatKit | Conversational interface |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              Next.js App + OpenAI ChatKit                        │   │
│  │         (Existing Phase II UI + New Chat Interface)              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/WebSocket
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         API GATEWAY LAYER                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Backend                               │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │   │
│  │  │  Auth Middleware│  │  CORS Middleware│  │ Rate Limiter    │ │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        AI AGENT LAYER                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                  OpenAI Agents SDK                               │   │
│  │  ┌───────────────────────────────────────────────────────────┐  │   │
│  │  │              AI Agent (Task Management Specialist)         │  │   │
│  │  │  - Natural Language Understanding                          │  │   │
│  │  │  - Intent Classification                                   │  │   │
│  │  │  - Tool Selection & Orchestration                          │  │   │
│  │  └───────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          MCP SERVER LAYER                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   MCP Protocol Handler                           │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │   │
│  │  │ add_task   │ │ list_tasks │ │complete_task│ │delete_task │   │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │   │
│  │  ┌────────────┐                                                  │   │
│  │  │update_task │                                                  │   │
│  │  └────────────┘                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       DATA ACCESS LAYER                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    SQLModel ORM                                  │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐                   │   │
│  │  │   Task     │ │Conversation│ │   Message  │                   │   │
│  │  │  (Phase II)│ │  (Phase III)│ │ (Phase III)│                   │   │
│  │  └────────────┘ └────────────┘ └────────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              Neon Serverless PostgreSQL                          │   │
│  │                    (Existing from Phase II)                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## User Scenarios & Testing

### User Story 1 - AI-Powered Task Creation (Priority: P1)

**As a** authenticated user,  
**I want** to create tasks by speaking naturally to an AI chatbot,  
**So that** I can quickly capture todos without filling out forms.

**Why this priority**: This is the core value proposition of Phase III - enabling frictionless task creation through natural language.

**Independent Test**: Can be fully tested by initiating a chat conversation, saying "Add a task to buy groceries tomorrow", and verifying the task appears in the database with correct title, description, and due date context.

**Acceptance Scenarios**:

1. **Given** an authenticated user opens the chat interface, **When** they type "I need to buy groceries tomorrow", **Then** the AI creates a task with title "Buy groceries" and appropriate metadata
2. **Given** a user requests task creation with multiple details, **When** they say "Schedule a team meeting for next Monday at 3pm in Conference Room A", **Then** the AI extracts and stores all relevant information in the task
3. **Given** the AI successfully creates a task, **When** the operation completes, **Then** the chatbot confirms the creation with task details in a natural response

---

### User Story 2 - AI Task Query & Listing (Priority: P1)

**As a** user,  
**I want** to ask the AI about my tasks in natural language,  
**So that** I can quickly understand what I need to do without navigating lists.

**Why this priority**: Essential for the conversational experience - users need to retrieve and understand their tasks through dialogue.

**Independent Test**: Can be fully tested by asking "What are my pending tasks?" and verifying the AI returns a formatted list of incomplete tasks from the database.

**Acceptance Scenarios**:

1. **Given** a user has existing tasks, **When** they ask "What do I need to do today?", **Then** the AI retrieves and presents tasks in a conversational format
2. **Given** a user asks about completed tasks, **When** they say "Show me what I've finished", **Then** the AI filters and displays only completed tasks
3. **Given** a user asks about specific tasks, **When** they say "Do I have a task about the meeting?", **Then** the AI searches and returns matching tasks

---

### User Story 3 - AI Task Completion & Updates (Priority: P2)

**As a** user,  
**I want** to mark tasks as complete or update them through conversation,  
**So that** I can manage my task lifecycle naturally.

**Why this priority**: Completes the task management lifecycle, enabling full CRUD operations through natural language.

**Independent Test**: Can be fully tested by saying "I finished the grocery task" and verifying the task's `completed` field is set to `true` in the database.

**Acceptance Scenarios**:

1. **Given** a user has an incomplete task, **When** they say "I'm done with task 1" or "Mark the grocery task as complete", **Then** the AI identifies the task and sets `completed=true`
2. **Given** a user wants to modify a task, **When** they say "Change the meeting task to 4pm instead", **Then** the AI updates the task description/title appropriately
3. **Given** a user wants to remove a task, **When** they say "Delete the grocery task", **Then** the AI removes the task from the database after confirmation

---

### User Story 4 - Secure Multi-Tenant AI Interaction (Priority: P2)

**As a** user,  
**I want** my AI interactions to be secure and my tasks to remain private,  
**So that** I can trust the system with my personal information.

**Why this priority**: Critical for maintaining user trust and data privacy in a multi-tenant environment.

**Independent Test**: Can be fully tested by creating two authenticated users, having each interact with the AI, and verifying that User A cannot access or modify User B's tasks through any AI operation.

**Acceptance Scenarios**:

1. **Given** an authenticated user session, **When** the AI executes any MCP tool, **Then** the `user_id` is automatically included and validated
2. **Given** a user attempts indirect access to another user's task, **When** they say "Show me task [UUID belonging to another user]", **Then** the system returns "Task not found" without revealing existence
3. **Given** a user's authentication expires, **When** they continue chatting, **Then** the system requires re-authentication before executing any task operations

---

### User Story 5 - Conversation History & Context (Priority: P3)

**As a** user,  
**I want** the AI to remember our conversation context,  
**So that** I can have natural multi-turn dialogues about my tasks.

**Why this priority**: Enhances user experience by enabling contextual conversations, though the core functionality works without it.

**Independent Test**: Can be fully tested by having a multi-turn conversation ("Add a task" → "What did I just add?" → "Complete that task") and verifying the AI maintains context across turns.

**Acceptance Scenarios**:

1. **Given** a conversation session, **When** the user references "that task" or "the one I just mentioned", **Then** the AI correctly resolves the reference using conversation history
2. **Given** a user starts a new conversation session, **When** they begin chatting, **Then** the conversation history is fresh (stateless per session)
3. **Given** a conversation exceeds context limits, **When** new messages arrive, **Then** the system gracefully handles truncation while maintaining functionality

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System MUST expose 5 MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task` | P0 |
| FR-002 | System MUST integrate OpenAI Agents SDK for natural language processing | P0 |
| FR-003 | System MUST maintain compatibility with existing Phase II SQLModel Task model | P0 |
| FR-004 | System MUST enforce user authentication on all AI-initiated operations | P0 |
| FR-005 | System MUST include `user_id` automatically in all MCP tool executions | P0 |
| FR-006 | System MUST create `Conversation` and `Message` models for stateless history tracking | P1 |
| FR-007 | System MUST provide REST API endpoints for chat session management | P1 |
| FR-008 | System MUST integrate with OpenAI ChatKit for frontend chat UI | P1 |
| FR-009 | System MUST validate task ownership before executing MCP operations | P0 |
| FR-010 | System MUST preserve existing Phase II REST API endpoints | P0 |
| FR-011 | System MUST handle ambiguous natural language gracefully with clarifying questions | P2 |
| FR-012 | System MUST provide structured error responses for failed AI operations | P1 |
| FR-013 | System MUST log all AI-initiated task operations for audit purposes | P2 |
| FR-014 | System MUST support WebSocket connections for real-time chat streaming | P2 |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | Response Time | AI task operations average < 3 seconds |
| NFR-002 | Availability | 99.9% uptime for chat endpoint |
| NFR-003 | Scalability | Support 1000 concurrent chat sessions |
| NFR-004 | Security | All data encrypted in transit (TLS) and at rest |
| NFR-005 | Data Isolation | 100% tenant isolation - zero cross-user data access |
| NFR-006 | Backward Compatibility | Zero breaking changes to Phase II API |

### Key Entities

| Entity | Description |
|--------|-------------|
| **MCP Server** | Implements Model Context Protocol to expose standardized tools to AI agents |
| **TaskAgent** | OpenAI Agent configured with MCP tools and task management instructions |
| **Conversation** | Database model storing chat session metadata (user_id, session_id, created_at) |
| **Message** | Database model storing individual messages (conversation_id, role, content, timestamp) |
| **MCP Tool Handler** | Python functions that execute CRUD operations with automatic user_id injection |
| **Auth Middleware** | FastAPI dependency that validates JWT tokens and extracts user context |

---

## Database Schema (Phase III Extensions)

### Existing Models (Phase II - Unchanged)

```python
# models.py (existing)
class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Critical for multi-tenancy
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
```

### New Models (Phase III)

```python
# models.py (Phase III additions)

class ConversationBase(SQLModel):
    """Base schema for conversation sessions."""
    user_id: str = Field(index=True, description="Owner of this conversation")
    session_id: str = Field(unique=True, index=True, description="Unique session identifier")

class Conversation(ConversationBase, table=True):
    """Conversation session for tracking AI chat history."""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")

class MessageBase(SQLModel):
    """Base schema for chat messages."""
    role: str = Field(description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(description="Message content")

class Message(MessageBase, table=True):
    """Individual message within a conversation."""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

class MessageRead(MessageBase):
    """Schema for returning message data."""
    id: uuid.UUID
    conversation_id: uuid.UUID
    created_at: datetime
```

### Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│      User           │       │       Task          │
│  (Phase II - Better Auth)  │                       │
│─────────────────────│       │─────────────────────│
│ id (PK)             │       │ id (PK)             │
│ email               │       │ user_id (FK→User)   │
│ ...                 │       │ title               │
└─────────────────────┘       │ description         │
         │                    │ completed           │
         │                    │ created_at          │
         │                    │ updated_at          │
         │                    └─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐
│   Conversation      │
│─────────────────────│
│ id (PK)             │
│ user_id (FK→User)   │
│ session_id (unique) │
│ created_at          │
│ updated_at          │
└─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐
│      Message        │
│─────────────────────│
│ id (PK)             │
│ conversation_id     │
│     (FK→Conversation)│
│ role                │
│ content             │
│ created_at          │
└─────────────────────┘
```

---

## MCP Tools Specification

### Tool Interface Definition

All MCP tools follow a standardized interface pattern:

```python
@tool()
def tool_name(ctx: Context, arg1: type, arg2: type) -> ReturnType:
    """Tool description for AI understanding.
    
    Args:
        ctx: MCP context containing user authentication
        arg1: Parameter description
        arg2: Parameter description
    
    Returns:
        Structured result object
    """
    # Implementation
```

### Tool 1: add_task

| Property | Value |
|----------|-------|
| **Name** | `add_task` |
| **Purpose** | Create a new task based on natural language request |
| **Input Schema** | `{ title: string, description?: string, user_id: string (auto-injected) }` |
| **Output Schema** | `{ id: uuid, title: string, description: string, completed: boolean, user_id: string, created_at: datetime, updated_at: datetime }` |
| **Security** | Creates task for authenticated user only; `user_id` auto-injected from auth context |
| **Error Cases** | - Missing title → ValidationError<br>- Database error → InternalError |

**Example Usage**:
```python
# AI Agent calls:
result = add_task(ctx, title="Buy groceries", description="Milk, eggs, bread")
# Returns: { id: "uuid-123", title: "Buy groceries", description: "Milk, eggs, bread", ... }
```

---

### Tool 2: list_tasks

| Property | Value |
|----------|-------|
| **Name** | `list_tasks` |
| **Purpose** | Retrieve all tasks for the authenticated user |
| **Input Schema** | `{ user_id: string (auto-injected), completed?: boolean (optional filter) }` |
| **Output Schema** | `{ tasks: Array<Task>, count: integer }` |
| **Security** | Returns only tasks belonging to authenticated user |
| **Error Cases** | - Database error → InternalError |

**Example Usage**:
```python
# AI Agent calls:
result = list_tasks(ctx, completed=False)
# Returns: { tasks: [...], count: 5 }
```

---

### Tool 3: complete_task

| Property | Value |
|----------|-------|
| **Name** | `complete_task` |
| **Purpose** | Mark a specific task as completed |
| **Input Schema** | `{ task_id: uuid, user_id: string (auto-injected) }` |
| **Output Schema** | `{ id: uuid, title: string, completed: true, updated_at: datetime }` |
| **Security** | Only allows completing tasks owned by authenticated user |
| **Error Cases** | - Task not found → NotFoundError<br>- Task belongs to another user → NotFoundError (security) |

**Example Usage**:
```python
# AI Agent calls:
result = complete_task(ctx, task_id="uuid-123")
# Returns: { id: "uuid-123", title: "Buy groceries", completed: true, ... }
```

---

### Tool 4: delete_task

| Property | Value |
|----------|-------|
| **Name** | `delete_task` |
| **Purpose** | Remove a specific task from the database |
| **Input Schema** | `{ task_id: uuid, user_id: string (auto-injected) }` |
| **Output Schema** | `{ success: boolean, deleted_id: uuid }` |
| **Security** | Only allows deleting tasks owned by authenticated user |
| **Error Cases** | - Task not found → NotFoundError<br>- Task belongs to another user → NotFoundError (security) |

**Example Usage**:
```python
# AI Agent calls:
result = delete_task(ctx, task_id="uuid-123")
# Returns: { success: true, deleted_id: "uuid-123" }
```

---

### Tool 5: update_task

| Property | Value |
|----------|-------|
| **Name** | `update_task` |
| **Purpose** | Modify properties of an existing task |
| **Input Schema** | `{ task_id: uuid, title?: string, description?: string, completed?: boolean, user_id: string (auto-injected) }` |
| **Output Schema** | `{ id: uuid, title: string, description: string, completed: boolean, updated_at: datetime }` |
| **Security** | Only allows updating tasks owned by authenticated user |
| **Error Cases** | - Task not found → NotFoundError<br>- Task belongs to another user → NotFoundError (security)<br>- Empty title → ValidationError |

**Example Usage**:
```python
# AI Agent calls:
result = update_task(ctx, task_id="uuid-123", description="Milk, eggs, bread, butter")
# Returns: { id: "uuid-123", title: "Buy groceries", description: "Milk, eggs, bread, butter", ... }
```

---

## API Endpoints Specification

### Chat Session Management

#### POST /api/v1/chat/sessions

Create a new chat session.

**Request**:
```http
POST /api/v1/chat/sessions
Authorization: Bearer <jwt_token>
Content-Type: application/json

{}  # Empty body, session_id auto-generated
```

**Response**:
```json
{
  "session_id": "uuid-abc123",
  "created_at": "2026-03-05T10:30:00Z"
}
```

---

#### GET /api/v1/chat/sessions/{session_id}/messages

Retrieve conversation history for a session.

**Request**:
```http
GET /api/v1/chat/sessions/{session_id}/messages
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "messages": [
    {
      "id": "uuid-msg-1",
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2026-03-05T10:31:00Z"
    },
    {
      "id": "uuid-msg-2",
      "role": "assistant",
      "content": "I've added a task: Buy groceries",
      "created_at": "2026-03-05T10:31:02Z"
    }
  ]
}
```

---

#### POST /api/v1/chat/sessions/{session_id}/messages

Send a message to the AI chatbot.

**Request**:
```http
POST /api/v1/chat/sessions/{session_id}/messages
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "content": "Add a task to buy groceries tomorrow"
}
```

**Response**:
```json
{
  "message": {
    "id": "uuid-msg-3",
    "role": "assistant",
    "content": "I've created a task: Buy groceries",
    "created_at": "2026-03-05T10:32:00Z"
  },
  "tool_calls": [
    {
      "tool": "add_task",
      "result": {
        "id": "uuid-task-123",
        "title": "Buy groceries"
      }
    }
  ]
}
```

---

#### DELETE /api/v1/chat/sessions/{session_id}

Delete a chat session and its messages.

**Request**:
```http
DELETE /api/v1/chat/sessions/{session_id}
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "success": true,
  "deleted_session_id": "uuid-abc123"
}
```

---

### MCP Server Endpoint

#### GET /mcp/manifest

Return MCP server manifest describing available tools.

**Request**:
```http
GET /mcp/manifest
```

**Response**:
```json
{
  "name": "todo-ai-mcp-server",
  "version": "1.0.0",
  "tools": [
    {
      "name": "add_task",
      "description": "Create a new task",
      "inputSchema": { ... }
    },
    {
      "name": "list_tasks",
      "description": "List all tasks for the user",
      "inputSchema": { ... }
    }
  ]
}
```

---

## Security Considerations

### Authentication Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│ FastAPI  │────▶│   Auth   │────▶│   MCP    │
│          │ JWT │  Middleware│     │  Verify  │     │  Tool    │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                           │
                                           ▼
                                    ┌──────────┐
                                    │ user_id  │
                                    │ extracted│
                                    └──────────┘
                                           │
                                           ▼
                                    ┌──────────┐
                                    │ Auto-    │
                                    │ injected │
                                    │ into MCP │
                                    │ tools    │
                                    └──────────┘
```

### Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Authentication** | JWT tokens validated on every chat endpoint request |
| **Authorization** | `user_id` extracted from JWT and auto-injected into all MCP tools |
| **Data Isolation** | All database queries filtered by `user_id`; no cross-tenant access |
| **Input Validation** | SQLModel validators on all input schemas |
| **Rate Limiting** | Token bucket algorithm: 100 requests/minute per user |
| **Audit Logging** | All AI-initiated task operations logged with timestamp, user_id, operation type |
| **Error Handling** | Generic error messages to prevent information leakage |

### Security Edge Cases

1. **Task UUID Injection**: If a user provides another user's task UUID, the system returns "Task not found" without confirming existence.
2. **Session Hijacking**: Session IDs are UUIDs with sufficient entropy; sessions are tied to `user_id`.
3. **Prompt Injection**: AI agent instructions include explicit security constraints to ignore attempts to bypass authentication.

---

## Integration Points

### Phase II Compatibility

| Component | Phase II | Phase III |
|-----------|----------|-----------|
| **Database** | Neon PostgreSQL | Same (unchanged) |
| **Task Model** | SQLModel Task | Same (unchanged) |
| **Authentication** | Better Auth | Same (unchanged) |
| **API Endpoints** | `/api/tasks/*` | Preserved + new `/api/chat/*` |
| **Frontend** | Next.js | Same + ChatKit integration |

### OpenAI ChatKit Integration

The frontend integrates OpenAI ChatKit with the following configuration:

```typescript
// frontend/components/ChatInterface.tsx
import { ChatKitProvider, ChatWidget } from '@openai/chatkit';

<ChatKitProvider
  apiUrl="http://localhost:8000/api/v1/chat"
  sessionEndpoint="/sessions"
  messagesEndpoint="/messages"
  authProvider={betterAuthProvider}
>
  <ChatWidget />
</ChatKitProvider>
```

---

## Success Criteria

| ID | Criterion | Measurement | Target |
|----|-----------|-------------|--------|
| SC-001 | AI correctly interprets task operations | % of successful natural language → tool mappings | ≥ 90% |
| SC-002 | Data isolation maintained | Cross-user access attempts blocked | 100% |
| SC-003 | Response time | Average latency for AI operations | < 3 seconds |
| SC-004 | Backward compatibility | Phase II API endpoints functional | 100% |
| SC-005 | Tool mapping accuracy | Natural language → correct MCP tool | ≥ 95% |
| SC-006 | Error rate | Failed AI operations / total operations | < 5% |
| SC-007 | User satisfaction | User testing feedback score | ≥ 4/5 |

---

## Testing Strategy

### Unit Tests

| Test Suite | Coverage |
|------------|----------|
| MCP Tools | 100% branch coverage for all 5 tools |
| Auth Middleware | All authentication scenarios |
| Database Models | All CRUD operations |
| Input Validation | All edge cases |

### Integration Tests

| Test Scenario | Description |
|---------------|-------------|
| End-to-end chat flow | User creates session → sends message → AI executes tool → response returned |
| Multi-tenant isolation | Two users interact simultaneously; verify no data leakage |
| Error handling | Invalid inputs, missing tasks, expired tokens |

### User Acceptance Tests

| UAT Scenario | Success Criteria |
|--------------|------------------|
| Natural task creation | User says "Remind me to call John tomorrow" → task created |
| Task listing | User asks "What do I have pending?" → correct list shown |
| Task completion | User says "I finished the John task" → task marked complete |
| Ambiguous requests | User says "Do that thing" → AI asks clarifying question |

---

## Deployment Considerations

### Environment Variables

```bash
# .env (Phase III additions)
OPENAI_API_KEY=sk-...
OPENAI_AGENT_MODEL=gpt-4o
MCP_SERVER_PORT=8000
CHATKIT_MAX_MESSAGES=50
```

### Dependencies (requirements.txt additions)

```txt
# Phase III additions
openai-agents>=0.0.1
mcp>=1.0.0
websockets>=12.0
```

### Database Migrations

```bash
# Run migrations to create Conversation and Message tables
python -m sqlmodel migrate
```

---

## Appendix A: Example Conversation Flow

```
User: "Add a task to buy groceries tomorrow"
  ↓
FastAPI receives POST /api/v1/chat/sessions/{id}/messages
  ↓
Auth middleware validates JWT, extracts user_id
  ↓
Message saved to database
  ↓
OpenAI Agent processes message
  ↓
Agent identifies intent: CREATE_TASK
  ↓
Agent calls MCP tool: add_task(title="Buy groceries", description="tomorrow")
  ↓
MCP tool injects user_id automatically
  ↓
Task created in database
  ↓
Agent generates response: "I've added a task: Buy groceries"
  ↓
Response saved to database
  ↓
Response returned to frontend
  ↓
ChatKit displays AI response
```

---

## Appendix B: MCP Tool Implementation Template

```python
from mcp import tool, Context
from sqlmodel import Session, select
from models import Task, Conversation, Message
from database import engine
from fastapi import HTTPException

@tool()
async def add_task(ctx: Context, title: str, description: str = None) -> dict:
    """Create a new task for the authenticated user.
    
    Args:
        title: The task title (required)
        description: Optional task description
    
    Returns:
        Created task object
    """
    # Extract user_id from context (auto-injected by auth middleware)
    user_id = ctx.metadata.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    with Session(engine) as session:
        task = Task(title=title, description=description, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump()

@tool()
async def list_tasks(ctx: Context, completed: bool = None) -> dict:
    """List all tasks for the authenticated user.
    
    Args:
        completed: Optional filter for completed/pending tasks
    
    Returns:
        Dictionary with tasks array and count
    """
    user_id = ctx.metadata.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            query = query.where(Task.completed == completed)
        tasks = session.exec(query).all()
        return {"tasks": [t.model_dump() for t in tasks], "count": len(tasks)}

# ... similar implementations for complete_task, delete_task, update_task
```

---

## Appendix C: Agent Instructions Template

```python
# Agent system instructions for task management
AGENT_INSTRUCTIONS = """
You are a helpful task management assistant integrated with a todo application.
Your purpose is to help users manage their tasks through natural conversation.

Available Tools:
- add_task: Create a new task (requires title, optional description)
- list_tasks: Retrieve user's tasks (optional completed filter)
- complete_task: Mark a task as completed (requires task_id)
- delete_task: Remove a task (requires task_id)
- update_task: Modify a task (requires task_id, optional fields to update)

Guidelines:
1. Always confirm actions before executing destructive operations (delete)
2. Ask clarifying questions when requests are ambiguous
3. Provide friendly, conversational responses
4. Never expose internal IDs or technical details unless asked
5. Respect user privacy - only access the authenticated user's data

Security Constraints:
- Never attempt to bypass authentication
- Never access tasks belonging to other users
- Never reveal system internals or tool implementation details
"""
```

---

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - standardized protocol for AI tool integration |
| **OpenAI Agents SDK** | Framework for building AI agents with tool-calling capabilities |
| **SQLModel** | Python ORM combining SQLAlchemy and Pydantic |
| **Neon** | Serverless PostgreSQL database provider |
| **Better Auth** | Authentication library used in Phase II |
| **ChatKit** | OpenAI's conversational UI component library |
| **Multi-tenant** | Architecture where multiple users share infrastructure but data is isolated |
