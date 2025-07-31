#!/bin/bash

echo "🚀 Starting MeTTa Flights Backend Servers"
echo "=========================================="

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check if ports are available
echo "Checking port availability..."
check_port 8000 || exit 1
check_port 8001 || exit 1

echo ""
echo "Starting servers..."

# Start Flight Search API (port 8000)
echo "📡 Starting Flight Search API on port 8000..."
cd "project copy" && python api.py &
FLIGHT_API_PID=$!

# Wait a moment for the first server to start
sleep 3

# Start Authentication API (port 8001)
echo "🔐 Starting Authentication API on port 8001..."
cd "../backend" && python api.py &
AUTH_API_PID=$!

echo ""
echo "✅ Both servers are starting..."
echo "   Flight Search API: http://localhost:8000"
echo "   Authentication API: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $FLIGHT_API_PID 2>/dev/null
    kill $AUTH_API_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handler
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait 