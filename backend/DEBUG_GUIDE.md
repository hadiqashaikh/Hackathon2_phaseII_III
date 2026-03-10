# Debug Guide for Chatbot API Errors

## ⚠️ CRITICAL ISSUE FOUND

Your logs show:
```
✗ OPENAI_API_KEY is missing or placeholder!
```

**Your `.env` file contains a placeholder API key:** `sk-placeholder-for-migration`

### 🔧 Immediate Fix Required

1. Get a valid OpenAI API key from: https://platform.openai.com/api-keys
2. Update your `backend/.env` file:
   ```
   OPENAI_API_KEY="sk-proj-your-actual-key-here"
   ```
3. Restart the server

---

## Files Created/Modified

1. **`backend/debug_api.py`** - New debug-enabled API server
2. **`backend/api/routers/chat.py`** - Enhanced logging in the `/api/chat` route

## How to Use

### Option 1: Run debug_api.py (Recommended)

This provides the most comprehensive diagnostics:

```bash
cd backend
python debug_api.py
```

**What it does:**
- ✅ Checks if `OPENAI_API_KEY` is present and valid
- ✅ Tests database connectivity
- ✅ Tests OpenAI API key validity
- ✅ Tests TodoAgent initialization
- ✅ Logs all chat requests with detailed step-by-step information
- ✅ Captures full stack traces for all errors

**Debug Endpoints Available:**
- `GET /debug/config` - Shows current configuration
- `GET /debug/test-db` - Tests database connectivity
- `GET /debug/test-openai` - Tests OpenAI API key
- `GET /debug/test-agent` - Tests TodoAgent initialization
- `GET /health` - Comprehensive health check

### Option 2: Run main.py (with enhanced logging)

The `chat.py` router now has enhanced logging, so even running the regular server will show detailed logs:

```bash
cd backend
uvicorn main:app --reload --log-level debug
```

## What to Look For

### 1. OPENAI_API_KEY Issues

**Symptom:** Error during agent initialization or API calls

**Check terminal for:**
```
✗ OPENAI_API_KEY is missing or placeholder!
```
or
```
✗ OpenAI API key is INVALID: AuthenticationError: ...
```

**Solution:** Update `.env` with a valid OpenAI API key:
```
OPENAI_API_KEY="sk-proj-your-actual-key-here"
```

### 2. DATABASE_URL Issues

**Symptom:** Error during conversation or message operations

**Check terminal for:**
```
✗ Database connection FAILED: OperationalError: ...
```

**Solution:** Verify `DATABASE_URL` in `.env` is correct and the database is accessible.

### 3. TodoAgentRunner Issues

**Symptom:** Error when calling tools or processing messages

**Check terminal for:**
```
✗ AI agent error: <ExceptionType>: <message>
Full traceback:
...
```

**Common causes:**
- Missing or invalid OpenAI API key
- MCP context not properly initialized
- Tool execution failures

## Example Debug Output

When a chat request is made, you'll see:

```
================================================================================
CHAT REQUEST STARTED at 2026-03-06T10:30:45.123456
  user_id: user_123
  request.message: Add a task to buy groceries...
  request.conversation_id: None
  ✓ Created new Conversation: abc-123-def
  ✓ Saved user message: ID=456
  → Calling TodoAgentRunner.process_message_sync()...
    - user_id: user_123
    - message: Add a task to buy groceries...
    - conversation_history length: 0
  ✓ TodoAgentRunner initialized
  
  [IF SUCCESS]
  ✓ AI agent processing successful
  ✓ Chat response generated. Tool calls: 1
CHAT REQUEST COMPLETED successfully
================================================================================

  [IF ERROR]
  ✗ AI agent error: AuthenticationError: Error code: 401 - {'error': {'message': 'Incorrect API key', ...}}
  Full traceback:
  Traceback (most recent call last):
    File "api/routers/chat.py", line 200, in chat
      agent_response = runner.process_message_sync(...)
    ...
================================================================================
```

## Quick Diagnostic Checklist

Run these commands in order:

```bash
# 1. Start the debug server
cd backend
python debug_api.py

# 2. In another terminal, test each component:
curl http://localhost:8000/debug/config
curl http://localhost:8000/debug/test-db
curl http://localhost:8000/debug/test-openai
curl http://localhost:8000/debug/test-agent
curl http://localhost:8000/health
```

## Next Steps

1. **Start `debug_api.py`**
2. **Reproduce the error** by using the chatbot
3. **Check terminal output** for detailed error messages
4. **Share the logs** if you need further assistance

The logs will show you exactly:
- Which step failed
- What exception was raised
- The full stack trace
- The root cause of the error
