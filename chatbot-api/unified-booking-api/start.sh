#!/bin/bash

echo "Starting Unified Booking API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export BACKEND_API_URL="http://localhost:8001"
export CHEAPEST_API_URL="http://localhost:8001"
export FASTEST_API_URL="http://localhost:8003"
export OPTIMIZED_API_URL="http://localhost:8002"
export SECRET_KEY="unified-booking-super-secret-key-2024"

# Start the API
echo "Starting Unified Booking API on port 8004..."
python main.py 