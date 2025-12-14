@echo off
REM Quick start script for Windows - runs all Task 2 components

echo Starting Fynd AI Feedback System...
echo.

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo WARNING: GEMINI_API_KEY is not set!
    echo Please set it with: set GEMINI_API_KEY=your-key-here
    echo.
    pause
    exit /b 1
)

echo [1/3] Starting Backend API...
start "Backend API" cmd /k "cd src\backend && ..\..\venv\Scripts\python.exe main.py"
timeout /t 3 /nobreak > nul

echo [2/3] Starting User Dashboard...
start "User Dashboard" cmd /k "venv\Scripts\streamlit.exe run src\dashboards\user_dashboard.py --server.port 8501"
timeout /t 3 /nobreak > nul

echo [3/3] Starting Admin Dashboard...
start "Admin Dashboard" cmd /k "venv\Scripts\streamlit.exe run src\dashboards\admin_dashboard.py --server.port 8502"

echo.
echo ===================================
echo All services started!
echo ===================================
echo Backend API:      http://localhost:8000
echo User Dashboard:   http://localhost:8501
echo Admin Dashboard:  http://localhost:8502
echo ===================================
echo.
echo Press any key to open dashboards in browser...
pause > nul

start http://localhost:8501
start http://localhost:8502

echo.
echo To stop all services, close the terminal windows.
