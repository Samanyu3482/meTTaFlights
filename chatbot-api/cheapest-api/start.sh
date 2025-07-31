#!/bin/bash

# Cheapest Flight Search & Booking API Startup Script

echo "🚀 Starting Cheapest Flight Search & Booking API..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, pydantic, httpx" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Check if port 8002 is available
echo "🔍 Checking port availability..."
if lsof -Pi :8002 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8002 is already in use. Stopping existing process..."
    lsof -ti:8002 | xargs kill -9
    sleep 2
fi

# Start the API server
echo "🌟 Starting API server on port 8002..."
echo "📖 API Documentation: http://localhost:8002/docs"
echo "🔍 Health Check: http://localhost:8002/api/cheapest/health"
echo "💡 For terminal interface, run: python main.py --terminal"
echo ""

python3 main.py 