from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from main import load_dataset, smart_search, search_all_flights
from airline_service import get_airline_for_route, get_all_airlines, get_airline_by_code

app = FastAPI(title="MeTTa Flight Search API", version="1.0.0")

# Add CORS middleware to allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3001"
    ],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the flight data when the API starts
try:
    load_dataset("Data/flights.metta")
    print("Flight data loaded successfully!")
except Exception as e:
    print(f"Error loading flight data: {e}")

def enhance_flights_with_airline_data(flights: List[Dict]) -> List[Dict]:
    """Add airline information to flight results"""
    enhanced_flights = []
    
    for flight in flights:
        # Get airline info for this route
        airline_info = get_airline_for_route(flight['source'], flight['destination'])
        
        # Create enhanced flight data
        enhanced_flight = flight.copy()
        if airline_info:
            enhanced_flight['airline'] = {
                'code': airline_info['code'],
                'name': airline_info['name'],
                'logo': airline_info['logo'],
                'description': airline_info['description']
            }
        
        enhanced_flights.append(enhanced_flight)
    
    return enhanced_flights

class FlightSearchRequest(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None

class AirlineInfo(BaseModel):
    code: str
    name: str
    logo: str
    description: str

class FlightResponse(BaseModel):
    year: str
    month: str
    day: str
    source: str
    destination: str
    cost: str
    airline: Optional[AirlineInfo] = None

@app.get("/")
def read_root():
    return {"message": "MeTTa Flight Search API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/flights/search", response_model=List[FlightResponse])
def search_flights(request: FlightSearchRequest):
    """
    Search flights using MeTTa knowledge base
    """
    try:
        # Convert empty strings to None
        source = request.source.upper() if request.source and request.source.strip() else None
        destination = request.destination.upper() if request.destination and request.destination.strip() else None
        
        results = smart_search(
            source=source,
            destination=destination,
            year=request.year,
            month=request.month,
            day=request.day
        )
        
        # Enhance results with airline data
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/all", response_model=List[FlightResponse])
def get_all_flights():
    """
    Get all flights from the knowledge base
    """
    try:
        results = search_all_flights()
        
        # Enhance results with airline data
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching flights: {str(e)}")

@app.get("/api/flights/source/{source}", response_model=List[FlightResponse])
def search_by_source_airport(source: str):
    """
    Search flights by source airport
    """
    try:
        results = smart_search(source=source.upper())
        
        # Enhance results with airline data
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/destination/{destination}", response_model=List[FlightResponse])
def search_by_destination_airport(destination: str):
    """
    Search flights by destination airport
    """
    try:
        results = smart_search(destination=destination.upper())
        
        # Enhance results with airline data
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/route/{source}/{destination}", response_model=List[FlightResponse])
def search_by_route(source: str, destination: str):
    """
    Search flights by source and destination
    """
    try:
        results = smart_search(source=source.upper(), destination=destination.upper())
        
        # Enhance results with airline data
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

# New airline-specific endpoints
@app.get("/api/airlines")
def get_airlines():
    """
    Get all available airlines
    """
    try:
        airlines = get_all_airlines()
        return {"airlines": airlines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching airlines: {str(e)}")

@app.get("/api/airlines/{airline_code}")
def get_airline_info(airline_code: str):
    """
    Get information about a specific airline
    """
    try:
        airline = get_airline_by_code(airline_code.upper())
        if airline:
            return airline
        else:
            raise HTTPException(status_code=404, detail=f"Airline {airline_code} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching airline: {str(e)}")

@app.get("/api/airlines/{airline_code}/routes")
def get_airline_routes(airline_code: str):
    """
    Get all routes for a specific airline
    """
    try:
        from airline_service import airline_service
        routes = airline_service.get_routes_for_airline(airline_code.upper())
        return {"airline_code": airline_code.upper(), "routes": routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching routes: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 