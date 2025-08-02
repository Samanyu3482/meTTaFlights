#!/usr/bin/env python3
"""
Optimized Flight Search API
Finds flights with the best balance of cost and time (optimized priority).
"""

import asyncio
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from schemas.flight_schemas import (
    FlightSearchRequest, FlightSearchResponse, FlightDetails, 
    AirlineInfo, PriorityType, CabinClass, PassengerInfo
)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta
import os
from services.user_service import user_service

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

# Service class for optimized flight search

# JWT token handling
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id, "token": token.credentials}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_user_passenger_info(user_id: str, token: str) -> PassengerInfo:
    """Get passenger information for the current user from backend database"""
    return await user_service.get_user_passenger_info(user_id, token)

@app.get("/api/optimized/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Optimized Flight Search API",
        "timestamp": datetime.now().isoformat(),
        "integrated_apis": {
            "search_api": "http://localhost:8000",
            "auth_api": "http://localhost:8001"
        }
    }

@app.post("/api/optimized/search")
async def search_optimized_flight(
    request: FlightSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for the optimized flight between two airports with user information
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
            return FlightSearchResponse(
                success=False,
                message=f"No flights found from {request.source} to {request.destination} on {request.day}/{request.month}/{request.year}",
                flight=None,
                total_flights=0,
                search_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                priority_type=PriorityType.OPTIMIZED,
                source=request.source,
                destination=request.destination,
                search_date=f"{request.year:04d}-{request.month:02d}-{request.day:02d}"
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
        
        # Calculate fare breakdown
        cost = float(optimized.get('cost', 0))
        base_fare = cost * 0.85  # 85% base fare, 15% taxes
        taxes = cost * 0.15
        
        # Create airline info object
        airline = AirlineInfo(
            code=airline_info.get('code', 'Unknown'),
            name=airline_info.get('name', 'Unknown Airline'),
            logo=airline_info.get('logo', ''),
            description=airline_info.get('description', '')
        )
        
        # Convert to unified FlightDetails format
        optimized_flight = FlightDetails(
            id=f"flight_{optimized.get('source', '')}_{optimized.get('destination', '')}_{optimized.get('year', '')}_{optimized.get('month', '')}_{optimized.get('day', '')}",
            source=optimized.get('source', ''),
            destination=optimized.get('destination', ''),
            year=optimized.get('year', ''),
            month=optimized.get('month', ''),
            day=optimized.get('day', ''),
            departure_time=optimized.get('takeoff', ''),
            arrival_time=optimized.get('landing', ''),
            duration=duration_str,
            duration_minutes=duration_minutes,
            cost=cost,
            currency="USD",
            base_fare=base_fare,
            taxes=taxes,
            total_fare=cost,
            airline=airline,
            flight_number=f"{airline_info.get('code', 'XX')}123",
            stops=optimized.get('stops', 0),
            is_connecting=optimized.get('is_connecting', False),
            connection_airport=optimized.get('connection_airport', ''),
            layover_hours=optimized.get('layover_hours', 0),
            segments=[],
            aircraft="Boeing 737",
            cabin_class=CabinClass.ECONOMY,
            available_seats=50,
            seat_class="Economy",
            baggage_allowance={"checked": 1, "carry_on": 1},
            refund_policy="Non-refundable",
            change_policy="Change fee applies",
            meal_included=True,
            entertainment=True,
            wifi_available=False,
            power_outlets=True,
            booking_class="Y",
            fare_basis="YOW",
            ticket_type="Electronic",
            search_timestamp=datetime.now(),
            valid_until=datetime.now() + timedelta(hours=24)
        )
        
        # Get user passenger information
        user_passenger = await get_user_passenger_info(current_user["user_id"], current_user["token"])
        
        search_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Add user passenger information to the response
        if optimized_flight:
            optimized_flight.passenger_info = user_passenger
        
        return FlightSearchResponse(
            success=True,
            message=f"Optimized flight found from {request.source} to {request.destination}",
            flight=optimized_flight,
            total_flights=len(flights),
            search_time_ms=search_time_ms,
            priority_type=PriorityType.OPTIMIZED,
            source=request.source,
            destination=request.destination,
            search_date=f"{request.year:04d}-{request.month:02d}-{request.day:02d}"
        )
        
    except Exception as e:
        search_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        return FlightSearchResponse(
            success=False,
            message=f"Error searching for optimized flight: {str(e)}",
            flight=None,
            total_flights=0,
            search_time_ms=search_time_ms,
            priority_type=PriorityType.OPTIMIZED,
            source=request.source,
            destination=request.destination,
            search_date=f"{request.year:04d}-{request.month:02d}-{request.day:02d}"
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