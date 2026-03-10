@echo off
echo Stopping existing backend server...
taskkill /F /FI "WINDOWTITLE eq uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend server...
cd /d C:\Users\Admin\Desktop\Hackathon2\phase-two\backend
call venv\Scripts\activate
uvicorn main:app --reload --port 8000
