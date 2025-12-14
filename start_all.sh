#!/bin/bash
# Quick start script for Linux/Mac/WSL - runs all Task 2 components

echo "Starting Fynd AI Feedback System..."
echo ""

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "WARNING: GEMINI_API_KEY is not set!"
    echo "Please set it with: export GEMINI_API_KEY=your-key-here"
    echo ""
    exit 1
fi

# Activate venv
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

echo "[1/3] Starting Backend API..."
cd src/backend
python main.py &
BACKEND_PID=$!
cd ../..
sleep 3

echo "[2/3] Starting User Dashboard..."
streamlit run src/dashboards/user_dashboard.py --server.port 8501 &
USER_PID=$!
sleep 3

echo "[3/3] Starting Admin Dashboard..."
streamlit run src/dashboards/admin_dashboard.py --server.port 8502 &
ADMIN_PID=$!

echo ""
echo "==================================="
echo "All services started!"
echo "==================================="
echo "Backend API:      http://localhost:8000"
echo "User Dashboard:   http://localhost:8501"
echo "Admin Dashboard:  http://localhost:8502"
echo "==================================="
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait and cleanup on exit
trap "kill $BACKEND_PID $USER_PID $ADMIN_PID 2>/dev/null; exit" INT TERM

wait
