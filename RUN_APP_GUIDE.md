# 🚀 Complete Setup Guide - Todo AI Chatbot (Ollama)

## ✅ Configuration Complete!

Aapka system ab **Ollama** (free, local AI) use kar raha hai. Koi API key expire nahi hogi!

---

## 📋 Step-by-Step Running Guide

### **Step 1: Ollama Server Start Karein**

Ollama ko run karna zaroori hai kyunki ye local AI model host karta hai.

```bash
# Naya terminal kholen aur ye chalayein:
ollama serve
```

**Expected Output:**
```
2026/03/09 23:30:00 INFO: serving on http://127.0.0.1:11434
```

**Note:** Ollama background mein automatically bhi chal sakta hai. Check karein:
```bash
ollama list
```

Agar model dikhe to Ollama chal raha hai!

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

### **Problem: "Ollama server not running"**

**Solution:**
```bash
# Ollama start karein
ollama serve

# Agar already chal raha hai to restart karein:
# Task Manager mein jaake "ollama" end karein, phir:
ollama serve
```

---

### **Problem: "Model not found" ya slow response**

**Solution:**
```bash
# Model dobara download karein
ollama pull qwen2.5:3b

# Ya koi aur model try karein:
ollama pull llama3.2
```

Phir `.env` update karein:
```env
OPENAI_AGENT_MODEL="llama3.2"
```

---

### **Problem: Backend 500 error de raha hai**

**Solution:**
1. Backend terminal check karein - error wahan dikhega
2. Ollama chal raha hai verify karein: `http://localhost:11434`
3. `.env` file check karein:
   ```env
   OPENAI_BASE_URL="http://localhost:11434/v1"
   OPENAI_AGENT_MODEL="qwen2.5:3b"
   ```

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

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Backend:**
```bash
cd C:\Users\Admin\Desktop\Hackathon2\phase-two\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 3 - Frontend:**
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
| Ollama | http://localhost:11434 | AI model server |

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

1. **Ollama hamesha chal raha hona chahiye** - Band karoge to AI kaam nahi karega

2. **Backend auto-reload hota hai** - Code changes se server restart nahi karna padta

3. **Frontend bhi auto-reload hota hai** - React changes automatically dikhenge

4. **Model quality improve karni hai?** To better model download karein:
   ```bash
   ollama pull llama3.1  # 8B model, better quality
   ```
   Phir `.env` mein:
   ```env
   OPENAI_AGENT_MODEL="llama3.1"
   ```

---

## 🆘 Still Having Issues?

1. **Check backend terminal** - Error wahan dikhega
2. **Check Ollama is running** - `ollama list` command chalayein
3. **Verify .env settings** - Sab paths sahi hone chahiye
4. **Restart all servers** - Teenon band karke phir start karein

---

## ✅ Success Indicators

**Sab kuch chal raha hai agar:**

- ✅ Ollama: `ollama list` shows models
- ✅ Backend: `http://localhost:8000/docs` opens Swagger UI
- ✅ Frontend: `http://localhost:3000` shows login page
- ✅ AI Chat: Message bhejne par reply aata hai aur task add hota hai

---

**Enjoy your FREE, unlimited AI chatbot! 🎉**
