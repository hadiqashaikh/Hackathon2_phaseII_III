# Data Model: Authentication System

## Overview
This document defines the database schema for the authentication system, including tables for users, sessions, accounts, and verification, designed to work with Better Auth and Drizzle ORM.

## Database Schema

### User Table
```sql
Table "user" {
  id UUID [pk, default: gen_random_uuid()]
  email VARCHAR(255) [not null, unique]
  email_verified BOOLEAN [default: false]
  name VARCHAR(255) [not null]
  password_hash VARCHAR(255) [not null]
  image_url TEXT
  created_at TIMESTAMP [default: `now()`]
  updated_at TIMESTAMP [default: `now()`]
}
```

**Description**: Stores user account information including authentication credentials and profile data.

**Key Constraints**:
- Email must be unique
- Email addresses must follow standard format validation
- Password hashes stored using secure algorithm (handled by Better Auth)
- Default values for timestamps and verification status

### Session Table
```sql
Table "session" {
  id UUID [pk, default: gen_random_uuid()]
  user_id UUID [not null, ref: > user.id]
  token VARCHAR(510) [not null, unique]
  expires_at TIMESTAMP [not null]
  created_at TIMESTAMP [default: `now()`]
  updated_at TIMESTAMP [default: `now()`]
}
```

**Description**: Manages active user sessions with JWT token information and expiration tracking.

**Key Constraints**:
- Token must be unique across all sessions
- Sessions linked to valid users via foreign key
- Automatic cleanup of expired sessions

### Account Table
```sql
Table "account" {
  id UUID [pk, default: gen_random_uuid()]
  user_id UUID [not null, ref: > user.id]
  provider_id VARCHAR(255) [not null]
  provider_account_id VARCHAR(255) [not null]
  access_token TEXT
  refresh_token TEXT
  id_token TEXT
  token_expires_at TIMESTAMP
  created_at TIMESTAMP [default: `now()`]
  updated_at TIMESTAMP [default: `now()`]
}
```

**Description**: Stores information about user accounts from external authentication providers (OAuth).

**Key Constraints**:
- Provider and provider account ID combination must be unique per user
- Accounts linked to valid users via foreign key
- Support for multiple providers per user

### Verification Table
```sql
Table "verification" {
  id UUID [pk, default: gen_random_uuid()]
  identifier VARCHAR(255) [not null]  // email, phone, etc.
  value VARCHAR(255) [not null]       // token, code, etc.
  type VARCHAR(50) [not null]         // email_verification, password_reset, etc.
  expires_at TIMESTAMP [not null]
  created_at TIMESTAMP [default: `now()`]
}
```

**Description**: Manages verification tokens for email verification, password resets, and other verification flows.

**Key Constraints**:
- Identifier and type combination helps manage different verification flows
- Automatic cleanup of expired verification tokens

## Drizzle Schema Implementation

### TypeScript Schema Definition
```typescript
// src/lib/schema.ts

import { pgTable, pgEnum, uuid, varchar, boolean, timestamp, text } from "drizzle-orm/pg-core";
import { sql } from "drizzle-orm";

// Enums if needed
export const verificationTypes = pgEnum("verification_type", [
  "email_verification",
  "password_reset",
  "two_factor",
  "invite"
]);

// User table
export const users = pgTable("user", {
  id: uuid("id").defaultRandom().primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  emailVerified: boolean("email_verified").default(false),
  name: varchar("name", { length: 255 }).notNull(),
  passwordHash: varchar("password_hash", { length: 255 }).notNull(),
  imageUrl: text("image_url"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Session table
export const sessions = pgTable("session", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  token: varchar("token", { length: 510 }).notNull().unique(),
  expiresAt: timestamp("expires_at").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Account table
export const accounts = pgTable("account", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  providerId: varchar("provider_id", { length: 255 }).notNull(),
  providerAccountId: varchar("provider_account_id", { length: 255 }).notNull(),
  accessToken: text("access_token"),
  refreshToken: text("refresh_token"),
  idToken: text("id_token"),
  tokenExpiresAt: timestamp("token_expires_at"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Verification table
export const verifications = pgTable("verification", {
  id: uuid("id").defaultRandom().primaryKey(),
  identifier: varchar("identifier", { length: 255 }).notNull(),
  value: varchar("value", { length: 255 }).notNull(),
  type: verificationTypes("type").notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

## Data Relationships

### Entity Relationship Diagram
```
users ─── accounts
  │         │
  │         │ (one-to-many: user can have multiple accounts)
  │
  │
  └── sessions
      │ (one-to-many: user can have multiple sessions)

users ─── verifications
  │         │
  │         │ (one-to-many: user can have multiple verification tokens)
```

## Multi-tenancy Considerations

### User Data Isolation
- All queries must filter by `user_id` to ensure data isolation
- Session management tied to specific user ID
- Account data linked to specific user ID
- Verification requests scoped to specific user context

### Access Control Patterns
- Primary access control: `WHERE user_id = $current_user_id`
- Row-level security: Additional database-level security if needed
- API-level validation: Backend services validate JWT and user context

## Security Considerations

### Password Security
- Passwords stored as secure hashes (handled by Better Auth)
- No plain text passwords stored in the database
- Use of secure algorithms for password hashing

### Token Security
- Session tokens stored securely with appropriate length
- Token expiration managed automatically
- Secure random token generation

### Verification Security
- Verification tokens expire after appropriate time limits
- One-time use for sensitive operations
- Rate limiting for verification requests

## Indexing Strategy

### Required Indexes
- `users.email`: For efficient user lookups by email
- `sessions.token`: For efficient session validation
- `sessions.expires_at`: For efficient cleanup of expired sessions
- `verifications.expires_at`: For efficient cleanup of expired verifications

### Performance Indexes
- `accounts.provider_id` and `accounts.provider_account_id`: For OAuth provider lookups
- `users.created_at`: For time-based queries
- `sessions.user_id`: For user session management