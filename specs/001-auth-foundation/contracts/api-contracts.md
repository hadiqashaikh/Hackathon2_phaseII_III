# API Contracts: Authentication System

## Overview
This document defines the API contracts for the authentication system, ensuring consistency between the Next.js frontend and the FastAPI backend that will validate JWT tokens.

## Authentication API Endpoints

### Registration API
```
POST /api/auth/sign-up
```

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (Success)**:
- Status: 200 OK
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "session": {
    "token": "jwt-token-string",
    "expiresAt": "2024-01-01T00:00:00.000Z"
  }
}
```

**Response (Error)**:
- Status: 400 Bad Request
```json
{
  "message": "Invalid email format"
}
```
- Status: 409 Conflict
```json
{
  "message": "User already exists"
}
```

### Login API
```
POST /api/auth/sign-in/email
```

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (Success)**:
- Status: 200 OK
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "session": {
    "token": "jwt-token-string",
    "expiresAt": "2024-01-01T00:00:00.000Z"
  }
}
```

**Response (Error)**:
- Status: 400 Bad Request
```json
{
  "message": "Invalid credentials"
}
```

### Session Verification API
```
GET /api/auth/session
```

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Response (Success)**:
- Status: 200 OK
```json
{
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "session": {
    "token": "jwt-token-string",
    "expiresAt": "2024-01-01T00:00:00.000Z"
  }
}
```

**Response (Error)**:
- Status: 401 Unauthorized
```json
{
  "message": "Unauthorized"
}
```

### Logout API
```
POST /api/auth/sign-out
```

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Response (Success)**:
- Status: 200 OK
```json
{
  "success": true
}
```

## JWT Token Structure

### Token Payload
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### Token Headers
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

## Token Validation Contract for FastAPI Backend

The FastAPI backend must be able to validate JWT tokens created by Better Auth using the same secret.

### Validation Algorithm
1. Extract JWT from Authorization header
2. Decode JWT using HS256 algorithm
3. Verify signature using BETTER_AUTH_SECRET
4. Check token expiration (exp claim)
5. Extract user information from token claims

### Validation Response
- Valid token: Continue with request processing
- Invalid token: Return 401 status with error message

### Error Responses from Backend
When validating a request with an auth token, the FastAPI backend should return:

- Status: 401 Unauthorized
```json
{
  "error": "Invalid authentication token",
  "code": "AUTH_001"
}
```

- Status: 401 Unauthorized (expired)
```json
{
  "error": "Authentication token has expired",
  "code": "AUTH_002"
}
```

## CORS Configuration

The authentication API should be configured to allow requests from:
- Frontend domain: `http://localhost:3000` (development)
- Frontend domain: `https://yourdomain.com` (production)

## Session Management

### Token Refresh
- Session tokens have a limited lifetime
- When a token expires, the client needs to re-authenticate
- Refresh token functionality may be implemented separately

### Concurrent Sessions
- Users can have multiple active sessions
- Each session has its own JWT token
- Session revocation should be supported for security

## Error Handling Consistency

### Client-Side Error Handling
All authentication API calls should have consistent error handling:

```typescript
type AuthError = {
  message: string;
  code?: string;
};
```

### Server-Side Error Responses
All authentication API responses should follow the same error structure:

```json
{
  "message": "Descriptive error message",
  "code": "Error code for client handling"
}
```

## Security Requirements

### Token Transmission
- JWT tokens must be transmitted via Authorization header
- HTTPS is required for all authentication requests
- Tokens should not be stored in local storage for sensitive operations

### Rate Limiting
- Authentication endpoints should implement rate limiting
- Limit: 5 attempts per minute per IP
- Temporarily block after 10 failed attempts

### Input Validation
- Email format validation (RFC 5322)
- Password strength requirements (min 8 characters, special chars optional)
- Input sanitization for all user-provided values