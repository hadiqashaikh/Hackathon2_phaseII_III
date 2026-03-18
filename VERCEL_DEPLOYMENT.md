# Vercel Deployment Guide - Todo AI Chatbot

## Quick Summary

All frontend API calls now use **relative paths** (e.g., `/api/chat/conversations`). Vercel will automatically route these to the Python backend.

## Required Environment Variables for Vercel

Add these to your **Vercel Project Dashboard**:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db?sslmode=require` |
| `BETTER_AUTH_SECRET` | Random secret (min 32 chars) | `5CwVsf6DKcEhtCMdq0oP5PsVfbi1wakF` |
| `BETTER_AUTH_URL` | Your Vercel app URL | `https://your-app.vercel.app` |
| `OPENROUTER_API_KEY` | OpenRouter API key | `sk-or-v1-xxxxxxxxxxx` |

## How to Add Environment Variables to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click **Settings** tab
4. Click **Environment Variables**
5. Click **Add New**
6. Add each variable:
   - **Name**: `DATABASE_URL`
   - **Value**: Your actual connection string
   - **Environments**: Check Production, Preview, and Development
7. Click **Save**
8. **Redeploy** your project for changes to take effect

## Project Structure

```
phase-two/
├── api/                    # Python FastAPI backend
│   ├── main.py            # Entry point for Vercel
│   ├── routers/           # API route handlers
│   ├── models.py          # Database models
│   ├── config.py          # Environment config
│   └── requirements.txt   # Python dependencies
├── my-todo/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App pages
│   │   └── lib/           # API client (uses relative paths)
│   └── .env               # Local dev env vars
├── vercel.json            # Vercel routing config
└── .env.example           # Template for env vars
```

## How Routing Works

### Local Development
```
Frontend (localhost:3000) → http://localhost:8001/api/* → Backend
```

### Vercel Production
```
Frontend (your-app.vercel.app) → /api/* → Python Serverless Function
```

The `vercel.json` configuration routes all `/api/*` requests to `api/main.py`.

## Files Modified for Vercel Compatibility

1. **`my-todo/src/lib/api.ts`** - Changed `BASE_URL` to empty string (relative paths)
2. **`my-todo/src/app/page.tsx`** - Changed `API_BASE` to empty string (relative paths)
3. **`api/main.py`** - Updated CORS to allow all origins (`["*"]`)
4. **`vercel.json`** - Added Python runtime configuration

## Deployment Checklist

- [ ] Add all 4 environment variables to Vercel
- [ ] Verify `requirements.txt` includes all dependencies
- [ ] Test locally with `vercel dev` (optional)
- [ ] Deploy to Vercel
- [ ] Check Vercel Functions logs for errors
- [ ] Test chat and task functionality

## Troubleshooting

### "Cannot connect to backend"
- Check that environment variables are set in Vercel
- Verify the Python function deployed successfully (check Vercel Functions tab)

### "CORS error"
- Already fixed with `allow_origins=["*"]` in `main.py`

### "Database connection failed"
- Ensure `DATABASE_URL` includes `?sslmode=require`
- Check that your database allows connections from Vercel IPs

### "AI processing failed"
- Verify `OPENROUTER_API_KEY` is correct
- Check OpenRouter account has credits

## Local Development

For local testing with the same configuration:

```bash
# Terminal 1 - Backend
cd api
uvicorn main:app --reload --host 127.0.0.1 --port 8001

# Terminal 2 - Frontend
cd my-todo
npm run dev
```

The frontend will use `http://localhost:8001` as fallback when `NEXT_PUBLIC_API_BASE_URL` is not set.
