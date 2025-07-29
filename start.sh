#!/bin/bash

echo "🚀 Starting MeTTa Flight Search System with Authentication..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $FLIGHT_BACKEND_PID $AUTH_BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the MeTTa flight search backend
echo "📡 Starting MeTTa Flight Search Backend (FastAPI) on port 8000..."
cd project
python api.py &
FLIGHT_BACKEND_PID=$!
cd ..

# Wait a moment for flight backend to start
sleep 3

# Check if flight backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Flight Search Backend is running on http://localhost:8000"
else
    echo "❌ Flight Search Backend failed to start"
    exit 1
fi

# Start the Authentication backend
echo "🔐 Starting Authentication Backend (FastAPI) on port 8001..."
cd backend
python api.py &
AUTH_BACKEND_PID=$!
cd ..

# Wait a moment for auth backend to start
sleep 3

# Check if auth backend is running
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ Authentication Backend is running on http://localhost:8001"
else
    echo "❌ Authentication Backend failed to start"
    exit 1
fi

# Start the Next.js frontend
echo "🌐 Starting Next.js Frontend..."
cd me-tt-a-flights
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 5

echo "🎉 MeTTa Flight Search System with Authentication is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Flight Search API: http://localhost:8000"
echo "🔐 Authentication API: http://localhost:8001"
echo "📚 Flight API Docs: http://localhost:8000/docs"
echo "📚 Auth API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to stop
wait 