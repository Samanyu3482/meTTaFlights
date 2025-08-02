#!/bin/bash

# MeTTa Flight Search & Booking System - Setup Verification Script
# This script verifies that all components are properly set up

echo "🔍 Verifying MeTTa Flight Search & Booking System Setup..."
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "WARNING" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

# Function to check if command exists
check_command() {
    local cmd=$1
    local name=$2
    if command -v $cmd &> /dev/null; then
        print_status "OK" "$name is installed"
        return 0
    else
        print_status "ERROR" "$name is not installed"
        return 1
    fi
}

# Function to check if file exists
check_file() {
    local file=$1
    local name=$2
    if [ -f "$file" ]; then
        print_status "OK" "$name exists"
        return 0
    else
        print_status "ERROR" "$name not found"
        return 1
    fi
}

# Function to check if directory exists
check_directory() {
    local dir=$1
    local name=$2
    if [ -d "$dir" ]; then
        print_status "OK" "$name exists"
        return 0
    else
        print_status "ERROR" "$name not found"
        return 1
    fi
}

echo ""
echo "📋 Checking Prerequisites..."
echo "---------------------------"

# Check required software
check_command "python" "Python"
check_command "node" "Node.js"
check_command "npm" "npm"
check_command "git" "Git"

echo ""
echo "📦 Checking Project Structure..."
echo "------------------------------"

# Check project structure
check_directory "backend" "Backend directory"
check_directory "chatbot-api" "Chatbot API directory"
check_directory "me-tt-a-flights" "Frontend directory"
check_directory "venv" "Virtual environment"
check_directory "details" "Details directory"

echo ""
echo "🔧 Checking API Components..."
echo "----------------------------"

# Check API directories
check_directory "chatbot-api/cheapest-api" "Cheapest API"
check_directory "chatbot-api/fastest-api" "Fastest API"
check_directory "chatbot-api/optimized-api" "Optimized API"
check_directory "chatbot-api/unified-booking-api" "Unified Booking API"

echo ""
echo "📄 Checking Configuration Files..."
echo "--------------------------------"

# Check requirements files
check_file "backend/requirements.txt" "Backend requirements.txt"
check_file "chatbot-api/cheapest-api/requirements.txt" "Cheapest API requirements.txt"
check_file "chatbot-api/fastest-api/requirements.txt" "Fastest API requirements.txt"
check_file "chatbot-api/optimized-api/requirements.txt" "Optimized API requirements.txt"
check_file "chatbot-api/unified-booking-api/requirements.txt" "Unified Booking API requirements.txt"
check_file "me-tt-a-flights/package.json" "Frontend package.json"

echo ""
echo "🗄️ Checking Database..."
echo "----------------------"

# Check database
if [ -f "backend/auth_database.db" ]; then
    print_status "OK" "Database file exists"
else
    print_status "WARNING" "Database file not found (will be created on first run)"
fi

echo ""
echo "📊 Checking Data Files..."
echo "------------------------"

# Check data files
check_file "project copy/Data_new/flights.metta" "Flight data file"
check_file "details/airports.csv" "Airports CSV"
check_file "details/metta_sample_flights.csv" "Sample flights CSV"

echo ""
echo "📚 Checking Documentation..."
echo "---------------------------"

# Check documentation
check_file "details/chatbot_apis_documentation.md" "API documentation"
check_file "details/api_descriptions.md" "API descriptions"
check_file "README.md" "Main README"

echo ""
echo "🚀 Checking Startup Scripts..."
echo "-----------------------------"

# Check startup scripts
check_file "start_all_services.sh" "Start script"
check_file "stop_all_services.sh" "Stop script"

# Make scripts executable
chmod +x start_all_services.sh stop_all_services.sh verify_setup.sh
print_status "OK" "Startup scripts are executable"

echo ""
echo "🔍 Checking Virtual Environment..."
echo "--------------------------------"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_status "OK" "Virtual environment is activated"
else
    print_status "WARNING" "Virtual environment is not activated"
    echo "   Run: source venv/bin/activate"
fi

echo ""
echo "🌐 Checking Port Availability..."
echo "------------------------------"

# Check if ports are available
for port in 3000 8000 8001 8002 8003 8005; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_status "WARNING" "Port $port is in use"
    else
        print_status "OK" "Port $port is available"
    fi
done

echo ""
echo "========================================================"
echo "🎯 Setup Verification Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. If virtual environment is not activated: source venv/bin/activate"
echo "2. Install dependencies if needed"
echo "3. Start all services: ./start_all_services.sh"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For detailed setup instructions, see README.md"
echo "========================================================" 