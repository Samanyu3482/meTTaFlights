#!/bin/bash

echo "🚀 Starting Optimized Flight Search API..."
echo "=========================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this script from the optimized-api directory."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if port 8004 is available
if lsof -Pi :8004 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8004 is already in use. Stopping existing process..."
    lsof -ti:8004 | xargs kill -9
    sleep 2
fi

echo "🌐 Starting API server on http://localhost:8004"
echo "📖 API Documentation: http://localhost:8004/docs"
echo "🔍 Health Check: http://localhost:8004/api/optimized/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the API server
python main.py 