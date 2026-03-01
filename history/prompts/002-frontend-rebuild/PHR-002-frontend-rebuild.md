---
id: PHR-002-frontend-rebuild
title: frontend-rebuild-spec
stage: spec
date: 2026-02-22
surface: cli
model: if/qwen3-coder-plus
feature: 002-frontend-rebuild
branch: 002-frontend-rebuild
user: Admin
command: /sp.specify
labels: [specification, frontend, todo-app]
links:
  spec: ../specs/002-frontend-rebuild/spec.md
  ticket:
  adr:
  pr:
files:
- path: specs/002-frontend-rebuild/spec.md
  action: created
  summary: Complete feature specification for frontend rebuild
- path: specs/002-frontend-rebuild/checklists/requirements.md
  action: created
  summary: Quality checklist for specification validation
tests:

---

## Prompt

Task: Fresh Frontend Rebuild in 'todo-app' folder

Context:
1. Directory: DO NOT use the folder named 'frontend' (it's locked). Create everything in a NEW folder named 'todo-app'.
2. Env Config: Use these EXACT values for '.env.local':
   BETTER_AUTH_SECRET="5CwVsf6DKcEhtCMdq0oP5PsVfbi1wakF"
   DATABASE_URL="postgresql://neondb_owner:npg_XM0r5pnEcRov@ep-cold-cell-ai60bn0x-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
   BETTER_AUTH_URL="http://localhost:3000"
   NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
   NEXT_PUBLIC_API_BASE_URL="http://localhost:3000"

3. Requirements:
   - Framework: Next.js 15 (App Router), Tailwind CSS, Lucide Icons.
   - Auth: Setup Better Auth client in 'src/lib/auth-client.tsx' (must be .tsx).
   - Database: Use Drizzle to connect to the EXISTING Neon tables (user, session, task).
   - UI: "Bhut Achi UI" - Create a modern, clean Dashboard. Use a Glassmorphism card for the Todo list.
   - Operations: Add, Toggle, and Delete tasks. Ensure tasks are filtered by 'userId'.

4. Fix Previous Errors:
   - No 'useAuth' hook (use session from authClient).
   - No absolute path issues (use @/ alias).

Goal: A fully functional, professional-looking Full-Stack Todo app.

## Response snapshot

Created complete feature specification for the frontend rebuild in the 'todo-app' directory. The specification includes user scenarios, functional requirements, key entities, and success criteria. The spec defines a Next.js 15 application with user authentication, task management operations, and a modern glassmorphism UI design. All requirements from the user input have been translated into clear, testable specifications without implementation details.

## Outcome

- ✅ Impact: Created complete feature specification for frontend rebuild
- 🧪 Tests:
- 📁 Files: 2 files created (spec and checklist)
- 🔁 Next prompts: /sp.plan, /sp.tasks
- 🧠 Reflection: Specification successfully created with all sections complete and no clarifications needed

## Evaluation notes (flywheel)

- Failure modes observed:
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):