<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
  - I. Spec-Driven Development → I. Agentic-Only Development
  - III. Security-First Authentication → III. Stateless Security
  - IV. Data Isolation and Persistence → IV. Multi-tenancy
  - VI. RESTful API Design → VI. Clean Separation
Added sections:
  - VII. Naming Conventions
  - VIII. Response Format Requirements
  - IX. Shared Secret Constraint
Removed sections: V. Test-First Development (NON-NEGOTIABLE)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->

# Hackathon 2 - Multi-User Full-Stack Todo Application Constitution

## Core Principles

### I. Agentic-Only Development
All code must be generated via spec-driven prompts; no manual edits. Development must follow the sequence: Specification → Plan → Tasks → Implementation, ensuring every change has a clear purpose and traceability. All implementation work must be performed using Claude Code agents following established templates and patterns.

### II. Clean Architecture Separation
Frontend (Next.js) and Backend (FastAPI) communicate strictly via REST API. Frontend and backend must remain completely separated with distinct concerns. Frontend uses Next.js 16+ with App Router, while backend uses Python FastAPI. Communication occurs exclusively through well-defined RESTful API contracts.

### III. Stateless Security
Authorization must be handled via JWT tokens verified by a shared secret. Authentication must be implemented using Better Auth with JWT tokens, following security best practices. All API endpoints require authentication verification, and JWT must be validated on every backend request to ensure secure access control. Tokens must be passed in the 'Authorization: Bearer <token>' header.

### IV. Multi-tenancy
Strict user isolation where data is filtered by user_id at the DB level. Each user's data must be strictly isolated using user ID filtering in all database queries. Data must persist reliably in Neon Serverless PostgreSQL with proper schema design ensuring data integrity and performance.

### V. RESTful API Design
All API endpoints must follow RESTful conventions with proper HTTP status codes (200, 201, 401, 404, etc.) and consistent request/response formats. APIs must be predictable, scalable, and well-documented.

## Additional Constraints and Standards

### Technology Stack Requirements
- Auth: Better Auth (TS) with JWT plugin enabled for backend interoperability
- Backend: Python 3.10+ FastAPI with SQLModel for type-safe ORM
- Database: Neon Serverless PostgreSQL with persistent storage
- Frontend: Next.js 16+ using the App Router
- Environment variables must be used for all secrets (BETTER_AUTH_SECRET)

### Naming Conventions
Use snake_case for Python and camelCase for TypeScript. All functions, variables, and class names must follow the appropriate naming convention based on the language being used.

### Response Format Requirements
All API errors must return clear status codes (e.g., 401 for invalid tokens). Error responses must include proper HTTP status codes and descriptive error messages to ensure consistent client behavior.

### Shared Secret Constraint
Both services MUST use the BETTER_AUTH_SECRET from .env for signing/verification. This ensures consistent JWT token validation across all application components.

### Performance and Reliability Standards
- All API endpoints must handle authentication efficiently without impacting performance
- Database queries must always be optimized and include proper indexing
- Frontend must provide responsive user experience with proper error handling
- Application must support multiple concurrent users with data isolation

## Development Workflow

### Code Review Process
- All code must pass through spec-driven validation before implementation
- Pull requests must demonstrate compliance with all constitutional principles
- Frontend and backend changes must be validated separately and together
- Authentication and data isolation requirements must be verified in all reviews

### Quality Gates
- All tests must pass before merging
- Security vulnerabilities must be addressed before approval
- Performance benchmarks must meet defined standards
- Code must follow established architectural patterns

## Governance

Constitution supersedes all other development practices. Amendments require explicit documentation, approval from project maintainers, and a migration plan if changes affect existing code. All pull requests and code reviews must verify compliance with constitutional principles. Complexity must be justified with clear rationale and documented trade-offs.

Success criteria:
- User can Sign up/Sign in and receive a valid JWT
- FastAPI backend rejects requests without a token or with a token from a different user
- All 5 Todo features (CRUD + Toggle) work seamlessly across the stack

**Version**: 1.1.0 | **Ratified**: 2026-02-18 | **Last Amended**: 2026-02-19
