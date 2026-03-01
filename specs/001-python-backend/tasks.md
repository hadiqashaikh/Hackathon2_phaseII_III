---
description: "Task list for Python Backend Development with JWT Verification and SQLModel"
---

# Tasks: Python Backend Development

**Input**: Design documents from `/specs/001-python-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend project**: `backend/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 [P] Create requirements.txt with fastapi, uvicorn, sqlmodel, python-jose[cryptography], psycopg2-binary dependencies
- [X] T003 Create .env file with BETTER_AUTH_SECRET and DATABASE_URL placeholders

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create database connection in backend/database.py with SQLModel and Neon PostgreSQL
- [X] T005 [P] Define Task SQLModel in backend/models.py with id, title, description, completed, and user_id fields
- [X] T006 Create JWT validation dependency in backend/security.py with get_current_user function
- [X] T007 [P] Implement main.py with FastAPI app and database initialization
- [X] T008 Create API router structure in backend/api/routers/tasks.py
- [X] T009 Configure environment variable loading in backend

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Task Access (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to access their tasks through the API with proper JWT token validation and data isolation

**Independent Test**: Can be fully tested by making an API request with a valid JWT token and verifying that only the user's own tasks are returned, and requests with invalid tokens are rejected.

### Implementation for User Story 1

- [X] T010 [P] [US1] Create GET /api/tasks endpoint in backend/api/routers/tasks.py to return user's tasks only
- [X] T011 [US1] Implement JWT token validation in the GET /api/tasks endpoint
- [X] T012 [US1] Add user_id filtering to ensure only user's tasks are returned
- [X] T013 [US1] Set up proper error responses for invalid JWT tokens (401)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management Operations (Priority: P1)

**Goal**: Enable authenticated users to create, read, update, and delete their tasks via the API

**Independent Test**: Can be fully tested by authenticating with a valid JWT token and performing all CRUD operations on tasks, ensuring that only the user's own tasks can be modified.

### Implementation for User Story 2

- [X] T014 [P] [US2] Create POST /api/tasks endpoint in backend/api/routers/tasks.py for task creation
- [X] T015 [P] [US2] Create GET /api/tasks/{task_id} endpoint in backend/api/routers/tasks.py for single task retrieval
- [X] T016 [P] [US2] Create PUT /api/tasks/{task_id} endpoint in backend/api/routers/tasks.py for task updates
- [X] T017 [P] [US2] Create DELETE /api/tasks/{task_id} endpoint in backend/api/routers/tasks.py for task deletion
- [X] T018 [US2] Implement user_id validation to ensure tasks can only be modified by their owners
- [X] T019 [US2] Add PATCH /api/tasks/{task_id}/toggle endpoint for toggling completion status

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Cross-User Data Isolation (Priority: P2)

**Goal**: Ensure users cannot access, modify, or delete tasks belonging to other users

**Independent Test**: Can be fully tested by attempting to access another user's data with your own JWT token and verifying that such access is prevented.

### Implementation for User Story 3

- [X] T020 [P] [US3] Enhance all task endpoints to verify user_id from token matches expected ownership
- [X] T021 [US3] Add comprehensive validation to prevent cross-user access attempts
- [X] T022 [US3] Implement proper error handling for unauthorized access attempts (404 when task exists but belongs to another user)
- [X] T023 [US3] Test edge cases where URL user_id doesn't match JWT user_id

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T024 [P] Add comprehensive error handling and logging to all endpoints
- [X] T025 Add input validation for all request fields (title length, description length, etc.)
- [X] T026 Add database indexing for improved performance (especially on user_id field)
- [X] T027 Update documentation and run validation from quickstart.md
- [X] T028 [P] Add additional security measures and audit logging

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Create GET /api/tasks endpoint in backend/api/routers/tasks.py to return user's tasks only"
Task: "Implement JWT token validation in the GET /api/tasks endpoint"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence