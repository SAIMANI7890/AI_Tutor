@echo off
echo ============================================
echo Restarting Backend Server
echo ============================================
echo.

echo Stopping any running uvicorn processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting backend server...
echo.

cd /d "%~dp0"
call ..\.venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
