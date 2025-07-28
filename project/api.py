from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from main import load_dataset, smart_search, search_all_flights
from airline_service import get_airline_for_route, get_all_airlines, get_airline_by_code, get_all_airlines_for_route, get_route_competition_info

app = FastAPI(title="MeTTa Flight Search API", version="2.0.0")

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
    """Add airline information to flight results with enhanced multi-airline support"""
    enhanced_flights = []
    
    for flight in flights:
        # Get airline info for this route (now with weighted random selection)
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
    frequency: Optional[float] = None

class RouteCompetitionInfo(BaseModel):
    route: str
    airlines: List[AirlineInfo]
    competition_level: str
    airline_count: int

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
    return {"message": "Enhanced MeTTa Flight Search API is running!", "version": "2.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Enhanced API is running", "version": "2.0.0"}

@app.post("/api/flights/search", response_model=List[FlightResponse])
def search_flights(request: FlightSearchRequest):
    """
    Search flights using MeTTa knowledge base with enhanced multi-airline support
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
        
        # Enhance results with airline data (now with weighted random selection)
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/all", response_model=List[FlightResponse])
def get_all_flights():
    """
    Get all flights from the knowledge base with enhanced airline data
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
    Search flights by source airport with enhanced airline data
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
    Search flights by destination airport with enhanced airline data
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
    Search flights by source and destination with enhanced airline data
    """
    try:
        results = smart_search(source=source.upper(), destination=destination.upper())
        
        # Enhance results with airline data
        enhanced_results = enhance_flights_with_airline_data(results)
        
        return enhanced_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

# Enhanced airline-specific endpoints
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

# New enhanced endpoints for multi-airline routes
@app.get("/api/routes/{source}/{destination}/airlines")
def get_route_airlines(source: str, destination: str):
    """
    Get all airlines that operate on a specific route
    """
    try:
        airlines = get_all_airlines_for_route(source.upper(), destination.upper())
        return {
            "route": f"{source.upper()}-{destination.upper()}",
            "airlines": airlines,
            "airline_count": len(airlines)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching route airlines: {str(e)}")

@app.get("/api/routes/{source}/{destination}/competition", response_model=RouteCompetitionInfo)
def get_route_competition(source: str, destination: str):
    """
    Get detailed competition information for a specific route
    """
    try:
        competition_info = get_route_competition_info(source.upper(), destination.upper())
        return competition_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching route competition: {str(e)}")

@app.get("/api/routes/competition/analysis")
def get_competition_analysis():
    """
    Get overall competition analysis across all routes
    """
    try:
        from airline_service import airline_service
        
        # Analyze competition levels
        competition_stats = {
            "monopoly": 0,
            "duopoly": 0,
            "competitive": 0,
            "highly_competitive": 0,
            "none": 0
        }
        
        total_routes = 0
        
        for route in airline_service.route_mapping.keys():
            source, destination = route.split('-')
            competition_info = get_route_competition_info(source, destination)
            competition_level = competition_info['competition_level']
            competition_stats[competition_level] += 1
            total_routes += 1
        
        # Calculate percentages
        competition_percentages = {}
        for level, count in competition_stats.items():
            if total_routes > 0:
                competition_percentages[level] = round((count / total_routes) * 100, 2)
            else:
                competition_percentages[level] = 0
        
        return {
            "total_routes": total_routes,
            "competition_stats": competition_stats,
            "competition_percentages": competition_percentages,
            "summary": {
                "most_competitive_routes": competition_stats["highly_competitive"],
                "least_competitive_routes": competition_stats["monopoly"],
                "average_airlines_per_route": round(sum([info['airline_count'] for info in [get_route_competition_info(route.split('-')[0], route.split('-')[1]) for route in airline_service.route_mapping.keys()]]) / total_routes, 2) if total_routes > 0 else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing competition: {str(e)}")

@app.get("/api/routes/popular")
def get_popular_routes():
    """
    Get popular routes with airline information
    """
    try:
        from airline_service import airline_service
        
        popular_routes = []
        for route, flight_count in airline_service.airline_data.get('top_routes', [])[:10]:
            source, destination = route.split('-')
            competition_info = get_route_competition_info(source, destination)
            
            popular_routes.append({
                "route": route,
                "source": source,
                "destination": destination,
                "flight_count": flight_count,
                "airlines": competition_info['airlines'],
                "competition_level": competition_info['competition_level'],
                "airline_count": competition_info['airline_count']
            })
        
        return {"popular_routes": popular_routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching popular routes: {str(e)}")

# Airport autocomplete endpoints
@app.get("/api/airports/search")
def search_airports(query: str = "", limit: int = 10):
    """
    Search airports by code, name, or city with autocomplete functionality
    """
    try:
        import json
        import os
        
        # Load airport data
        airports_file = "airports.json"
        if not os.path.exists(airports_file):
            return {"airports": [], "total": 0}
        
        with open(airports_file, 'r') as f:
            airport_data = json.load(f)
        
        airports = airport_data.get('airports', [])
        
        if not query or len(query.strip()) == 0:
            # Return popular airports if no query
            popular_codes = ["JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SFO", "CLT", "LAS", "MCO"]
            popular_airports = [ap for ap in airports if ap['code'] in popular_codes]
            return {"airports": popular_airports[:limit], "total": len(popular_airports)}
        
        query = query.strip().upper()
        results = []
        
        for airport in airports:
            # Search by airport code
            if query in airport['code']:
                results.append(airport)
            # Search by airport name
            elif query in airport['name'].upper():
                results.append(airport)
            # Search by city
            elif query in airport['city'].upper():
                results.append(airport)
            # Search by state
            elif query in airport['state']:
                results.append(airport)
        
        # Sort results: exact code matches first, then partial matches
        def sort_key(airport):
            if airport['code'] == query:
                return 0  # Exact code match
            elif airport['code'].startswith(query):
                return 1  # Code starts with query
            elif airport['city'].upper().startswith(query):
                return 2  # City starts with query
            else:
                return 3  # Other matches
        
        results.sort(key=sort_key)
        
        return {"airports": results[:limit], "total": len(results)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching airports: {str(e)}")

@app.get("/api/airports/{airport_code}")
def get_airport_info(airport_code: str):
    """
    Get information about a specific airport by code
    """
    try:
        import json
        import os
        
        airports_file = "airports.json"
        if not os.path.exists(airports_file):
            raise HTTPException(status_code=404, detail="Airport data not found")
        
        with open(airports_file, 'r') as f:
            airport_data = json.load(f)
        
        airports = airport_data.get('airports', [])
        
        for airport in airports:
            if airport['code'].upper() == airport_code.upper():
                return airport
        
        raise HTTPException(status_code=404, detail=f"Airport {airport_code} not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching airport: {str(e)}")

@app.get("/api/airports")
def get_all_airports():
    """
    Get all airports (for debugging/testing)
    """
    try:
        import json
        import os
        
        airports_file = "airports.json"
        if not os.path.exists(airports_file):
            return {"airports": [], "total": 0}
        
        with open(airports_file, 'r') as f:
            airport_data = json.load(f)
        
        return airport_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching airports: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 