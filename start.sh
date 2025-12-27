#!/bin/bash

echo "========================================"
echo "   GearGuard - Starting Servers"
echo "========================================"
echo

echo "[1/2] Starting Flask Backend (Port 5000)..."
cd backend
python3 app.py &
BACKEND_PID=$!
sleep 3

echo "[2/2] Starting React Frontend (Port 3000)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
sleep 3

echo
echo "========================================"
echo "   Servers Started Successfully!"
echo "========================================"
echo
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"

# Function to cleanup processes
cleanup() {
    echo
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait