#!/usr/bin/env python3
"""
Optimized Flight Search API
Finds flights with the best balance of cost and time (optimized priority).
"""

import asyncio
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(
    title="Optimized Flight Search API",
    description="API to find flights with the best balance of cost and time",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlightSearchRequest(BaseModel):
    source: str
    destination: str
    year: int
    month: int
    day: int
    priority: str = "optimized"  # Always prioritize optimized balance
    include_connections: bool = True
    max_connections: int = 2

class OptimizedFlightResponse(BaseModel):
    success: bool
    message: str
    optimized_flight: Optional[Dict[str, Any]] = None
    total_flights: int = 0
    search_time_ms: float = 0

@app.get("/api/optimized/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Optimized Flight Search API",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/optimized/search")
async def search_optimized_flight(request: FlightSearchRequest):
    """
    Search for the optimized flight between two airports
    """
    start_time = datetime.now()
    
    try:
        # Validate inputs
        if not request.source or not request.destination:
            raise HTTPException(status_code=400, detail="Source and destination are required")
        
        if request.source == request.destination:
            raise HTTPException(status_code=400, detail="Source and destination cannot be the same")
        
        # Search for flights using the search API
        async with httpx.AsyncClient() as client:
            search_payload = {
                "source": request.source.upper(),
                "destination": request.destination.upper(),
                "year": request.year,
                "month": request.month,
                "day": request.day,
                "priority": "optimized",  # Focus on optimized balance
                "include_connections": request.include_connections
            }
            
            response = await client.post(
                "http://localhost:8000/api/flights/search",
                json=search_payload,
                timeout=10.0
            )
            response.raise_for_status()
            flights = response.json()
        
        if not flights:
            return OptimizedFlightResponse(
                success=False,
                message=f"No flights found from {request.source} to {request.destination} on {request.day}/{request.month}/{request.year}",
                total_flights=0,
                search_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )
        
        # The search API already returns flights sorted by optimized priority
        # The first flight is the most optimized (best balance of cost and time)
        optimized = flights[0]
        
        # Calculate proper duration (duration is in minutes from the search API)
        duration_minutes = optimized.get('duration', 0)
        
        if isinstance(duration_minutes, (int, float)) and duration_minutes > 0:
            # Convert minutes to hours and minutes
            hours = duration_minutes // 60
            minutes = duration_minutes % 60
            
            if minutes > 0:
                duration_str = f"{hours}h {minutes}m"
            else:
                duration_str = f"{hours}h"
        else:
            duration_str = "N/A"
        
        # Get airline information from the flight data
        airline_info = optimized.get('airline', {})
        
        # Convert to our expected format
        optimized_flight = {
            "id": f"flight_{optimized.get('source', '')}_{optimized.get('destination', '')}_{optimized.get('year', '')}_{optimized.get('month', '')}_{optimized.get('day', '')}",
            "source": optimized.get('source', ''),
            "destination": optimized.get('destination', ''),
            "year": optimized.get('year', ''),
            "month": optimized.get('month', ''),
            "day": optimized.get('day', ''),
            "takeoff": optimized.get('takeoff', ''),
            "landing": optimized.get('landing', ''),
            "duration": duration_str,
            "duration_minutes": duration_minutes,
            "cost": optimized.get('cost', ''),
            "airline": airline_info.get('code', 'Unknown'),
            "airline_name": airline_info.get('name', 'Unknown Airline'),
            "airline_logo": airline_info.get('logo', ''),
            "airline_description": airline_info.get('description', ''),
            "flight_number": f"{airline_info.get('code', 'XX')}123",
            "stops": optimized.get('stops', 0),
            "departure_time": optimized.get('takeoff', ''),
            "arrival_time": optimized.get('landing', ''),
            "is_connecting": optimized.get('is_connecting', False),
            "connection_airport": optimized.get('connection_airport', ''),
            "layover_hours": optimized.get('layover_hours', 0)
        }
        
        search_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        return OptimizedFlightResponse(
            success=True,
            message=f"Optimized flight found from {request.source} to {request.destination}",
            optimized_flight=optimized_flight,
            total_flights=len(flights),
            search_time_ms=search_time_ms
        )
        
    except Exception as e:
        search_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        return OptimizedFlightResponse(
            success=False,
            message=f"Error searching for optimized flight: {str(e)}",
            search_time_ms=search_time_ms
        )

@app.get("/api/optimized/search")
async def search_optimized_flight_get(
    source: str = Query(..., description="Source airport code"),
    destination: str = Query(..., description="Destination airport code"),
    year: int = Query(..., description="Year"),
    month: int = Query(..., description="Month"),
    day: int = Query(..., description="Day"),
    include_connections: bool = Query(True, description="Include connecting flights"),
    max_connections: int = Query(2, description="Maximum number of connections")
):
    """
    GET endpoint for optimized flight search
    """
    request = FlightSearchRequest(
        source=source,
        destination=destination,
        year=year,
        month=month,
        day=day,
        include_connections=include_connections,
        max_connections=max_connections
    )
    return await search_optimized_flight(request)

@app.get("/api/optimized/airlines")
async def get_airlines():
    """Get list of all airlines"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/airlines")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch airlines: {str(e)}"}

@app.get("/api/optimized/routes")
async def get_routes():
    """Get list of all available routes"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/routes")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch routes: {str(e)}"}

# Terminal interface for manual testing
async def terminal_interface():
    """Terminal interface for manual flight search"""
    print("Optimized Flight Search System")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Search for optimized flight")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            await search_flight_terminal()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

async def search_flight_terminal():
    """Terminal interface for flight search"""
    print("\nFlight Search")
    print("-" * 20)
    
    try:
        source = input("Enter source airport code (e.g., JFK): ").strip().upper()
        destination = input("Enter destination airport code (e.g., LAX): ").strip().upper()
        
        # Get date components separately
        day = int(input("Enter day (1-31): ").strip())
        month = int(input("Enter month (1-12): ").strip())
        year = int(input("Enter year (e.g., 2024): ").strip())
        
        # Create request
        request = FlightSearchRequest(
            source=source,
            destination=destination,
            year=year,
            month=month,
            day=day
        )
        
        print(f"\nSearching for optimized flights from {source} to {destination} on {day}/{month}/{year}...")
        print("Finding the best balance of cost and time...")
        
        result = await search_optimized_flight(request)
        
        if result.success:
            flight = result.optimized_flight
            print(f"SUCCESS: {result.message}")
            print(f"   Airline: {flight['airline']}")
            print(f"   Flight: {flight['flight_number']}")
            print(f"   Duration: {flight['duration']}")
            print(f"   Cost: ${flight['cost']}")
            print(f"   Stops: {flight['stops']}")
            print(f"   Departure: {flight['departure_time']}")
            print(f"   Arrival: {flight['arrival_time']}")
            print(f"   Total flights found: {result.total_flights}")
        else:
            print(f"ERROR: {result.message}")
            
    except ValueError as e:
        print(f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimized Flight Search API")
    parser.add_argument("--terminal", action="store_true", help="Run in terminal mode")
    args = parser.parse_args()
    
    if args.terminal:
        # Run terminal interface
        asyncio.run(terminal_interface())
    else:
        # Run API server
        print("Starting Optimized Flight API Server...")
        print("API Documentation: http://localhost:8004/docs")
        print("Health Check: http://localhost:8004/api/optimized/health")
        print("For terminal interface, run: python main.py --terminal")
        uvicorn.run(app, host="0.0.0.0", port=8004) 