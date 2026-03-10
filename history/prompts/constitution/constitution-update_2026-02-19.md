---
id: constitution-update-2026-02-19
title: Constitution Update
stage: constitution
date: 2026-02-19
surface: 50
model: if/qwen3-coder-plus
feature: hackathon2-todo-app
branch: main
user: Admin
command: /sp.constitution
labels: [constitution, governance, template]
links:
  spec:
  ticket:
  adr:
  pr:
files:
  - path: .specify/memory/constitution.md
    operation: edit
    description: Updated constitution with project-specific principles
tests:

---

## Prompt

/sp.constitution

Project: Hackathon 2 - Multi-User Full-Stack Todo Application

Core principles:
- Agentic-Only Development: All code must be generated via spec-driven prompts; no manual edits.
- Stateless Security: Authorization must be handled via JWT tokens verified by a shared secret.
- Multi-tenancy: Strict user isolation where data is filtered by user_id at the DB level.
- Clean Separation: Frontend (Next.js) and Backend (FastAPI) communicate strictly via REST API.

Key standards:
- Auth: Better Auth (TS) with JWT plugin enabled for backend interoperability.
- Backend: Python 3.10+ FastAPI with SQLModel for type-safe ORM.
- Database: Neon Serverless PostgreSQL with persistent storage.
- Token Handling: JWT tokens must be passed in the 'Authorization: Bearer <token>' header.
- Naming Conventions: Use snake_case for Python and camelCase for TypeScript.

Constraints:
- Shared Secret: Both services MUST use the BETTER_AUTH_SECRET from .env for signing/verification.
- Response Format: All API errors must return clear status codes (e.g., 401 for invalid tokens).
- Frontend: Must be Next.js 16+ using the App Router.

Success criteria:
- User can Sign up/Sign in and receive a valid JWT.
- FastAPI backend rejects requests without a token or with a token from a different user.
- All 5 Todo features (CRUD + Toggle) work seamlessly across the stack.

## Response snapshot

I've updated the project constitution to reflect the specific requirements of the Hackathon 2 - Multi-User Full-Stack Todo Application. The following changes were made:

- Version updated from 1.0.0 to 1.1.0 (minor version bump due to principle additions and modifications)
- Core principle I renamed from "Spec-Driven Development" to "Agentic-Only Development" with updated description
- Core principle III renamed from "Security-First Authentication" to "Stateless Security" with updated description
- Core principle IV renamed from "Data Isolation and Persistence" to "Multi-tenancy" with updated description
- Core principle VI renamed from "RESTful API Design" to "Clean Separation" with updated description
- Added new principle VII: Naming Conventions
- Added new principle VIII: Response Format Requirements
- Added new principle IX: Shared Secret Constraint
- Removed the Test-First Development principle (as it wasn't specified in the requirements)
- Updated the technology stack requirements to match the specified standards
- Added the success criteria to the governance section

The constitution template has been fully populated with the specific project details and requirements.

## Outcome

- ✅ Impact: Updated constitution with project-specific principles
- 🧪 Tests:
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts:
- 🧠 Reflection: Constitution now accurately reflects the project requirements

## Evaluation notes (flywheel)

- Failure modes observed:
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):