#!/bin/bash

# MeTTa Flight Search & Booking System - Startup Script
# This script starts all the required services for the application

echo "🚀 Starting MeTTa Flight Search & Booking System..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run the setup first."
    echo "   Run: python -m venv venv && source venv/bin/activate"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use. Stopping existing process..."
        lsof -ti:$port | xargs kill -9
        sleep 2
    fi
}

# Function to start a service
start_service() {
    local service_name=$1
    local port=$2
    local command=$3
    
    echo "🔧 Starting $service_name on port $port..."
    check_port $port
    
    # Start the service in background
    cd $command
    python main.py > ../${service_name}.log 2>&1 &
    local pid=$!
    echo $pid > ../${service_name}.pid
    cd ..
    
    # Wait a moment for service to start
    sleep 3
    
    # Check if service started successfully
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
        echo "✅ $service_name started successfully (PID: $pid)"
    else
        echo "❌ Failed to start $service_name"
        return 1
    fi
}

# Function to start backend
start_backend() {
    echo "🔧 Starting Backend Authentication & Booking API on port 8000..."
    check_port 8000
    
    cd backend
    python api.py > ../backend.log 2>&1 &
    local pid=$!
    echo $pid > ../backend.pid
    cd ..
    
    sleep 3
    
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend started successfully (PID: $pid)"
    else
        echo "❌ Failed to start Backend"
        return 1
    fi
}

# Function to start frontend
start_frontend() {
    echo "🔧 Starting Next.js Frontend on port 3000..."
    check_port 3000
    
    cd me-tt-a-flights
    npm run dev > ../frontend.log 2>&1 &
    local pid=$!
    echo $pid > ../frontend.pid
    cd ..
    
    sleep 5
    
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend started successfully (PID: $pid)"
    else
        echo "❌ Failed to start Frontend"
        return 1
    fi
}

# Create logs directory
mkdir -p logs

# Start all services
echo ""
echo "🔄 Starting all services..."

# Start Backend
start_backend
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Backend. Check backend.log for details."
    exit 1
fi

# Start Search APIs
start_service "Cheapest API" "8001" "chatbot-api/cheapest-api"
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Cheapest API. Check Cheapest\ API.log for details."
    exit 1
fi

start_service "Fastest API" "8003" "chatbot-api/fastest-api"
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Fastest API. Check Fastest\ API.log for details."
    exit 1
fi

start_service "Optimized API" "8002" "chatbot-api/optimized-api"
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Optimized API. Check Optimized\ API.log for details."
    exit 1
fi

start_service "Unified Booking API" "8005" "chatbot-api/unified-booking-api"
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Unified Booking API. Check Unified\ Booking\ API.log for details."
    exit 1
fi

# Start Frontend
start_frontend
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Frontend. Check frontend.log for details."
    exit 1
fi

echo ""
echo "🎉 All services started successfully!"
echo "=================================================="
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "💰 Cheapest API: http://localhost:8001"
echo "⚡ Fastest API: http://localhost:8003"
echo "🎯 Optimized API: http://localhost:8002"
echo "📋 Unified Booking API: http://localhost:8005"
echo ""
echo "📚 API Documentation:"
echo "   Backend: http://localhost:8000/docs"
echo "   Cheapest: http://localhost:8001/docs"
echo "   Fastest: http://localhost:8003/docs"
echo "   Optimized: http://localhost:8002/docs"
echo "   Unified Booking: http://localhost:8005/docs"
echo ""
echo "📝 Log files are saved in the project root:"
echo "   - backend.log"
echo "   - frontend.log"
echo "   - Cheapest API.log"
echo "   - Fastest API.log"
echo "   - Optimized API.log"
echo "   - Unified Booking API.log"
echo ""
echo "🛑 To stop all services, run: ./stop_all_services.sh"
echo "==================================================" 