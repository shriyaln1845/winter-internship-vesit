@echo off
cd /d "%~dp0"
echo Starting Diabetes Risk App...
echo Open your browser to http://127.0.0.1:8000
uvicorn app:app --reload --host 127.0.0.1 --port 8000
pause
