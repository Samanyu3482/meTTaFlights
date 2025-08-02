#!/bin/bash

# MeTTa Flight Search & Booking System - Stop Script
# This script stops all the running services

echo "🛑 Stopping MeTTa Flight Search & Booking System..."
echo "=================================================="

# Function to stop a service
stop_service() {
    local service_name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "🛑 Stopping $service_name (PID: $pid)..."
            kill -TERM $pid
            sleep 2
            
            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                echo "⚠️  Force stopping $service_name..."
                kill -9 $pid
            fi
            
            echo "✅ $service_name stopped"
        else
            echo "ℹ️  $service_name is not running"
        fi
        rm -f "$pid_file"
    else
        echo "ℹ️  $service_name PID file not found"
    fi
}

# Stop all services
echo "🔄 Stopping all services..."

# Stop Backend
stop_service "Backend" "backend.pid"

# Stop Search APIs
stop_service "Cheapest API" "Cheapest API.pid"
stop_service "Fastest API" "Fastest API.pid"
stop_service "Optimized API" "Optimized API.pid"
stop_service "Unified Booking API" "Unified Booking API.pid"

# Stop Frontend
stop_service "Frontend" "frontend.pid"

# Kill any remaining processes on our ports
echo "🧹 Cleaning up any remaining processes on our ports..."

for port in 3000 8000 8001 8002 8003 8005; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Killing process on port $port..."
        lsof -ti:$port | xargs kill -9
    fi
done

echo ""
echo "✅ All services stopped successfully!"
echo "=================================================="
echo "📝 Log files are still available in the project root:"
echo "   - backend.log"
echo "   - frontend.log"
echo "   - Cheapest API.log"
echo "   - Fastest API.log"
echo "   - Optimized API.log"
echo "   - Unified Booking API.log"
echo ""
echo "🚀 To start all services again, run: ./start_all_services.sh"
echo "==================================================" 