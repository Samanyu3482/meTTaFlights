#!/bin/bash

echo "🚀 Starting Fastest Flight Search API..."
echo "========================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this script from the fastest-api directory."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if port 8003 is available
if lsof -Pi :8003 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8003 is already in use. Stopping existing process..."
    lsof -ti:8003 | xargs kill -9
    sleep 2
fi

echo "🌐 Starting API server on http://localhost:8003"
echo "📖 API Documentation: http://localhost:8003/docs"
echo "🔍 Health Check: http://localhost:8003/api/fastest/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the API server
python main.py 