# Start Backend Server
@echo off
echo Starting Todo AI Chatbot Backend...
echo.

cd /d "%~dp0"

echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
