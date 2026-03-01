# Quickstart Guide: Authentication Foundation

## Overview
This guide provides step-by-step instructions to set up the Next.js authentication foundation with Better Auth and JWT support for cross-platform compatibility with FastAPI backend.

## Prerequisites
- Node.js 18+ installed
- A Neon PostgreSQL database instance
- `pnpm` or `npm` package manager
- Environment variables for database connection and auth secrets

## Step 1: Initialize Next.js Project

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd frontend
```

## Step 2: Install Dependencies

```bash
npm install better-auth @better-auth/drizzle-adapter drizzle-orm @neondatabase/serverless drizzle-kit
npm install -D @types/node
```

## Step 3: Set Up Environment Variables

Create `.env.local` file in the frontend directory:

```env
# Database Configuration
DATABASE_URL="your_neon_database_url_here"

# Better Auth Configuration
BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_SECRET="your_super_secret_key_here_must_be_at_least_32_characters_long"

# Neon Database Authentication
NEON_DATABASE_URL="your_neon_database_url_here"
```

## Step 4: Create Database Connection

Create `src/lib/db.ts`:

```typescript
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.NEON_DATABASE_URL!);
export const db = drizzle(sql);
```

## Step 5: Define Authentication Schema

Create `src/lib/schema.ts` with the schema defined in the data-model.md file.

## Step 6: Configure Better Auth

Create `src/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "@better-auth/drizzle-adapter";
import { db } from "@/lib/db";
import { accounts, sessions, users, verifications } from "@/lib/schema";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: {
      user: users,
      account: accounts,
      session: sessions,
      verification: verifications,
    },
  }),
  secret: process.env.BETTER_AUTH_SECRET,
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET,
    }),
  ],
});
```

## Step 7: Create API Route Handler

Create `app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/auth";
import { NextRequest } from "next/server";

const handler = auth();
export { handler as GET, handler as POST, handler as PUT, handler as DELETE };
```

## Step 8: Sync Database Schema

Run the following command to create and sync the authentication tables:

```bash
npx drizzle-kit push
```

## Step 9: Environment Configuration

Ensure your `.env.local` has the proper configuration:

```env
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your_32_char_secret_key_here
NEON_DATABASE_URL=your_neon_db_connection_string
```

## Step 10: Test Authentication Setup

1. Start the development server:
```bash
npm run dev
```

2. Visit `http://localhost:3000/api/auth/session` to check if the auth API is working.

3. Test registration endpoint at `http://localhost:3000/api/auth/sign-up`.

## FastAPI Backend Integration

For backend compatibility with FastAPI, ensure the same BETTER_AUTH_SECRET is used in the FastAPI service for JWT validation.

Example FastAPI JWT validation:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token_data = jwt.decode(
            credentials.credentials,
            "your_better_auth_secret",
            algorithms=["HS256"]
        )
        return token_data
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

## Troubleshooting

### Common Issues:

1. **Database Connection Errors**:
   - Verify NEON_DATABASE_URL is correctly set
   - Check that your Neon database is accessible

2. **JWT Compatibility Issues**:
   - Ensure the same BETTER_AUTH_SECRET is used across all services
   - Verify JWT algorithms match (HS256)

3. **Session Management**:
   - Check that CORS settings allow your frontend domain
   - Verify auth endpoints are accessible

4. **Schema Sync Issues**:
   - Run `npx drizzle-kit introspect` to check current schema
   - Use `npx drizzle-kit push` to sync schema to database

## Next Steps

- Implement protected routes in your Next.js app
- Create authentication-aware UI components
- Connect to your FastAPI backend for JWT validation
- Add user profile management features
- Implement password reset functionality

## Verification Checklist

- [ ] Next.js app runs without errors
- [ ] Authentication API routes are accessible
- [ ] User registration and login work
- [ ] JWT tokens are generated and validated
- [ ] Database schema is properly synced
- [ ] Cross-platform JWT compatibility verified with FastAPI