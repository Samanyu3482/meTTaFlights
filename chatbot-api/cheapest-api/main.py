from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import httpx
import asyncio
import json
from datetime import datetime, timedelta
import requests
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
    title="Cheapest Flight Search API",
    description="API for finding the cheapest flights from project copy API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service class for cheapest flight search

class CheapestFlightService:
    def __init__(self):
        # Connect to your existing search API
        self.search_api_url = "http://localhost:8000"  # Your project copy API
    
    async def search_cheapest_flight(self, request: FlightSearchRequest) -> FlightSearchResponse:
        """Search for flights and return the cheapest one"""
        
        start_time = datetime.now()
        
        try:
            # Format date from day, month, year
            date_str = f"{request.year:04d}-{request.month:02d}-{request.day:02d}"
            
            # Call your existing search API
            search_response = await self._call_search_api(request.source, request.destination, date_str, request.passengers)
            
            if not search_response or not search_response.get('flights'):
                return FlightSearchResponse(
                    success=False,
                    message="No flights found for the given criteria",
                    flight=None,
                    total_flights=0,
                    search_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                    priority_type=PriorityType.CHEAPEST,
                    source=request.source,
                    destination=request.destination,
                    search_date=date_str
                )
            
            # Find the cheapest flight from results
            flights = search_response['flights']
            cheapest_flight = self._find_cheapest_flight(flights)
            
            if not cheapest_flight:
                return FlightSearchResponse(
                    success=False,
                    message="No flights available",
                    flight=None,
                    total_flights=len(flights),
                    search_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                    priority_type=PriorityType.CHEAPEST,
                    source=request.source,
                    destination=request.destination,
                    search_date=date_str
                )
            
            search_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            return FlightSearchResponse(
                success=True,
                message=f"Found cheapest flight: {cheapest_flight.airline.name} for ${cheapest_flight.cost}",
                flight=cheapest_flight,
                total_flights=len(flights),
                search_time_ms=search_time_ms,
                priority_type=PriorityType.CHEAPEST,
                source=request.source,
                destination=request.destination,
                search_date=date_str
            )
            
        except Exception as e:
            return FlightSearchResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
                flight=None,
                total_flights=0,
                search_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                priority_type=PriorityType.CHEAPEST,
                source=request.source,
                destination=request.destination,
                search_date=date_str
            )
    
    async def _call_search_api(self, source: str, destination: str, date: str, passengers: int) -> Dict[str, Any]:
        """Call your existing search API"""
        async with httpx.AsyncClient() as client:
            try:
                # Parse date components
                year, month, day = date.split('-')
                
                # Adjust this URL and payload to match your existing search API
                search_payload = {
                    "source": source,
                    "destination": destination,
                    "year": int(year),
                    "month": int(month),
                    "day": int(day),
                    "priority": "cost",  # Focus on cheapest flights
                    "include_connections": True
                }
                
                response = await client.post(
                    f"{self.search_api_url}/api/flights/search",  # Correct endpoint
                    json=search_payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return {"flights": response.json()}
                
            except httpx.RequestError as e:
                raise Exception(f"Search API unavailable: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Search API error: {e.response.text}")
    
    def _find_cheapest_flight(self, flights: List[Dict[str, Any]]) -> Optional[FlightDetails]:
        """Find the cheapest flight from the list"""
        if not flights:
            return None
        
        # Sort by cost (convert to float for comparison)
        sorted_flights = sorted(flights, key=lambda x: float(x.get('cost', float('inf'))))
        cheapest = sorted_flights[0]
        
        # Calculate proper duration (duration is in minutes from the search API)
        duration_minutes = cheapest.get('duration', 0)
        
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
        airline_info = cheapest.get('airline', {})
        
        # Calculate fare breakdown
        cost = float(cheapest.get('cost', 0))
        base_fare = cost * 0.85  # 85% base fare, 15% taxes
        taxes = cost * 0.15
        
        # Create airline info object
        airline = AirlineInfo(
            code=airline_info.get('code', 'Unknown'),
            name=airline_info.get('name', 'Unknown Airline'),
            logo=airline_info.get('logo', ''),
            description=airline_info.get('description', '')
        )
        
        # Convert to unified FlightDetails format using REAL data from project copy API
        flight_data = {
            "id": f"flight_{cheapest.get('source', '')}_{cheapest.get('destination', '')}_{cheapest.get('year', '')}_{cheapest.get('month', '')}_{cheapest.get('day', '')}",
            "source": cheapest.get('source', ''),
            "destination": cheapest.get('destination', ''),
            "year": cheapest.get('year', ''),
            "month": cheapest.get('month', ''),
            "day": cheapest.get('day', ''),
            "departure_time": cheapest.get('takeoff', ''),
            "arrival_time": cheapest.get('landing', ''),
            "duration": duration_str,
            "duration_minutes": duration_minutes,
            "cost": cost,
            "currency": "USD",
            "base_fare": base_fare,
            "taxes": taxes,
            "total_fare": cost,
            "airline": airline,
            "flight_number": f"{airline_info.get('code', 'XX')}123",
            "stops": cheapest.get('stops', 0),
            "is_connecting": cheapest.get('is_connecting', False),
            "connection_airport": cheapest.get('connection_airport', ''),
            "layover_hours": cheapest.get('layover_hours', 0),
            "aircraft": "Boeing 737",
            "cabin_class": CabinClass.ECONOMY,
            "available_seats": 50,
            "seat_class": "Economy",
            "baggage_allowance": {"checked": 1, "carry_on": 1},
            "refund_policy": "Non-refundable",
            "change_policy": "Change fee applies",
            "meal_included": True,
            "entertainment": True,
            "wifi_available": False,
            "power_outlets": True,
            "booking_class": "Y",
            "fare_basis": "YOW",
            "ticket_type": "Electronic",
            "search_timestamp": datetime.now(),
            "valid_until": datetime.now() + timedelta(hours=24)
        }
        
        return FlightDetails(**flight_data)

# Initialize service
cheapest_service = CheapestFlightService()

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

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Cheapest Flight Search API",
        "version": "1.0.0",
        "status": "healthy",
        "integrated_apis": {
            "search_api": "http://localhost:8000",
            "auth_api": "http://localhost:8001"
        }
    }

@app.post("/api/cheapest/search")
async def search_cheapest_flight(
    request: FlightSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for flights and return the cheapest one with user information
    """
    try:
        # Get user passenger information
        user_passenger = await get_user_passenger_info(current_user["user_id"], current_user["token"])
        
        # Search for flights
        result = await cheapest_service.search_cheapest_flight(request)
        
        # Add user passenger information to the response
        if result.success and result.flight:
            result.flight.passenger_info = user_passenger
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/cheapest/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "cheapest-flight-search",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "integrated_apis": {
            "search_api": "http://localhost:8000"
        }
    }

# Terminal interface for manual testing
async def terminal_interface():
    """Terminal interface for manual flight search"""
    print("Cheapest Flight Search System")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Search for cheapest flight")
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
        source = input("From (e.g., New York): ").strip()
        destination = input("To (e.g., London): ").strip()
        
        # Get date components separately
        day = int(input("Day (1-31): ").strip())
        month = int(input("Month (1-12): ").strip())
        year = int(input("Year (e.g., 2024): ").strip())
        
        passengers = int(input("Number of passengers: ").strip())
        
        request = FlightSearchRequest(
            source=source,
            destination=destination,
            day=day,
            month=month,
            year=year,
            passengers=passengers
        )
        
        print(f"\nSearching for flights from {source} to {destination} on {day}/{month}/{year}...")
        print("Finding the cheapest flight...")
        
        result = await cheapest_service.search_cheapest_flight(request)
        
        if result["success"]:
            flight = result["cheapest_flight"]
            print(f"SUCCESS: {result['message']}")
            print(f"   Airline: {flight['airline']}")
            print(f"   Flight: {flight['flight_number']}")
            print(f"   Price: ${flight['price']:.0f}")
            print(f"   Duration: {flight['duration']}")
            print(f"   Stops: {flight['stops']}")
            print(f"   Departure: {flight['departure_time']}")
            print(f"   Arrival: {flight['arrival_time']}")
            print(f"   Total flights found: {result['total_flights']}")
        else:
            print(f"ERROR: {result['message']}")
            
    except ValueError as e:
        print(f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Check if running in terminal mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--terminal":
        # Run terminal interface
        asyncio.run(terminal_interface())
    else:
        # Run API server
        print("Starting Cheapest Flight API Server...")
        print("API Documentation: http://localhost:8002/docs")
        print("Health Check: http://localhost:8002/api/cheapest/health")
        print("For terminal interface, run: python main.py --terminal")
        uvicorn.run(app, host="0.0.0.0", port=8002) 