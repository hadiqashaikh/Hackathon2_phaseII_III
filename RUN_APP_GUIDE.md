# 🚀 Complete Setup Guide - Todo AI Chatbot (OpenRouter)

## ✅ Configuration Complete!

Aapka system ab **OpenRouter** (free cloud AI) use kar raha hai. Koi API key expire nahi hogi!

**Note:** Agar OpenRouter API key nahi hai, toh local development ke liye Ollama use kar sakte ho (commented section in `.env`).

---

## 📋 Step-by-Step Running Guide

### **Step 1: OpenRouter API Key Lo (Optional for Cloud)**

Agar cloud deployment karna hai toh OpenRouter API key lo:

1. Visit: https://openrouter.ai/
2. Sign up (Google se 2 min)
3. API Key copy karo
4. `.env` file mein paste karo: `OPENROUTER_API_KEY=sk-or-...`

**Note:** Local testing ke liye API key zaroori nahi - aap Ollama use kar sakte ho!

---

### **Step 2: Backend Server Start Karein**

```bash
# Navigate to backend folder
cd C:\Users\Admin\Desktop\Hackathon2\phase-two\backend

# Activate virtual environment
venv\Scripts\activate

# Start backend
uvicorn main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal OPEN!** Backend chal raha hona chahiye.

---

### **Step 3: Frontend Server Start Karein**

```bash
# NEW terminal kholen
cd C:\Users\Admin\Desktop\Hackathon2\phase-two\my-todo

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**Expected Output:**
```
- Local:   http://localhost:3000
- Ready in 3s
```

**Keep this terminal OPEN too!**

---

### **Step 4: Browser Mein Test Karein**

1. **Browser open karein:** `http://localhost:3000`

2. **Login karein** (agar pehle se logged in nahi hain)

3. **AI Chat page par jayein:** Header mein "🤖 AI Chat" button click karein

4. **Test messages bhejein:**
   ```
   Add a task to buy milk
   ```
   
   ```
   Show me my tasks
   ```
   
   ```
   Delete my first task
   ```

---

## 🔧 Troubleshooting

### **Problem: "OpenRouter API key not set"**

**Solution:**
1. `.env` file check karo - `OPENROUTER_API_KEY` add karo
2. Ya local testing ke liye Ollama use karo (uncomment Ollama section in `.env`)

---

### **Problem: "Model not found" ya slow response**

**Solution:**
```bash
# OpenRouter pe different free model try karo:
# .env mein update karo:
OPENROUTER_AGENT_MODEL="llama-3-8b-instruct"
```

Available free models: https://openrouter.ai/models

---

### **Problem: Backend 500 error de raha hai**

**Solution:**
1. Backend terminal check karein - error wahan dikhega
2. `.env` file check karein - API key set hai?
3. Database connection check karein

---

### **Problem: Frontend "Failed to connect" error**

**Solution:**
1. Backend chal raha hai verify karein: `http://localhost:8000/docs`
2. Browser console check karein (F12 → Console)
3. Dono servers running hone chahiye:
   - Backend: port 8000
   - Frontend: port 3000

---

## 📁 Quick Reference

### **Servers Start Karne Ka Quick Command:**

**Terminal 1 - Backend:**
```bash
cd C:\Users\Admin\Desktop\Hackathon2\phase-two\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd C:\Users\Admin\Desktop\Hackathon2\phase-two\my-todo
npm run dev
```

---

### **Important URLs:**

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main app |
| Backend API | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger docs |
| OpenRouter | https://openrouter.ai | Cloud AI API |

---

## 🎯 Features Test Karein

### **1. Task Creation:**
```
Add a task to buy groceries
```

### **2. List Tasks:**
```
Show me all my tasks
```

### **3. Complete Task:**
```
Mark the first task as complete
```

### **4. Delete Task:**
```
Delete the task about groceries
```

### **5. Update Task:**
```
Update the first task to say "buy milk and eggs"
```

---

## 💡 Tips

1. **OpenRouter API key optional hai** - Local testing ke liye Ollama use kar sakte ho

2. **Backend auto-reload hota hai** - Code changes se server restart nahi karna padta

3. **Frontend bhi auto-reload hota hai** - React changes automatically dikhenge

4. **Model quality improve karni hai?** OpenRouter pe better free model try karo:
   ```env
   OPENROUTER_AGENT_MODEL="llama-3-8b-instruct"
   ```

---

## 🆘 Still Having Issues?

1. **Check backend terminal** - Error wahan dikhega
2. **Verify .env settings** - API key aur database URL check karo
3. **Restart servers** - Dono band karke phir start karein

---

## ✅ Success Indicators

**Sab kuch chal raha hai agar:**

- ✅ Backend: `http://localhost:8000/docs` opens Swagger UI
- ✅ Frontend: `http://localhost:3000` shows login page
- ✅ AI Chat: Message bhejne par reply aata hai aur task add hota hai

---

**Enjoy your FREE AI chatbot! 🎉**
