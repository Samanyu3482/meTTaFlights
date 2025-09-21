from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from hyperon import MeTTa, ExpressionAtom
import os
import glob
from datetime import datetime, timedelta
import sqlite3

# Initialize FastAPI app
app = FastAPI(
    title="Flight Search API",
    description="A powerful flight search API with connecting flights support",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)

# Add CORS middleware to allow requests from the chatbot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Initialize MeTTa
metta = MeTTa()
metta.run("!(bind! &space (new-space))")



class Credentials(BaseModel):
    username: str
    mpin: str


class BookingRequest(BaseModel):
    username: str
    flight_details: dict 


# Pydantic Models for Request/Response
class FlightSearchRequest(BaseModel):
    source: Optional[str] = Field(None, description="Source airport code (e.g., 'PHX')")
    destination: Optional[str] = Field(None, description="Destination airport code (e.g., 'BUR')")
    year: Optional[int] = Field(None, description="Year (e.g., 2025)")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month (1-12)")
    day: Optional[int] = Field(None, ge=1, le=31, description="Day (1-31)")
    airline: Optional[str] = Field(None, description="Airline name (e.g., 'United_Airlines')")
    priority: Optional[str] = Field("cost", description="Sort priority: 'cost', 'time', or 'optimized'")
    include_connections: Optional[bool] = Field(True, description="Include connecting flights")

class FlightSegment(BaseModel):
    source: str
    destination: str
    takeoff: str
    landing: str
    duration: int
    cost: str
    airline: str

class Flight(BaseModel):
    year: str
    month: str
    day: str
    source: str
    destination: str
    cost: str
    departure: str
    arrival: str
    airline: str
    duration_minutes: int
    is_connecting: bool
    connection_airport: Optional[str] = None
    layover_hours: Optional[float] = None
    airlines: Optional[List[str]] = None
    segments: Optional[List[FlightSegment]] = None

class FlightSearchResponse(BaseModel):
    success: bool
    count: int
    flights: List[Flight]

class AirlinesResponse(BaseModel):
    success: bool
    airlines: List[str]

class AirportsResponse(BaseModel):
    success: bool
    airports: List[str]

class HealthResponse(BaseModel):
    status: str
    message: str

# Core Functions
def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
        
    paths = []
    if os.path.isfile(path) and path.endswith(".metta"):
        paths.append(path)
    else:
        paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    
    for file_path in paths:
        try:
            metta.run(f"!(load-ascii &space {file_path})")
        except Exception as e:
            raise Exception(f"Error loading '{file_path}': {e}")

def calculate_flight_duration(takeoff_time: str, landing_time: str) -> int:
    try:
        if not takeoff_time or not landing_time:
            return 240
        
        takeoff_padded = takeoff_time.zfill(4)
        landing_padded = landing_time.zfill(4)
        
        takeoff_hour = int(takeoff_padded[:2])
        takeoff_minute = int(takeoff_padded[2:])
        landing_hour = int(landing_padded[:2])
        landing_minute = int(landing_padded[2:])
        
        takeoff_total = takeoff_hour * 60 + takeoff_minute
        landing_total = landing_hour * 60 + landing_minute
        
        if landing_total < takeoff_total:
            landing_total += 24 * 60
            
        duration = landing_total - takeoff_total
        
        if duration < 0 or duration > 24 * 60:
            return 240
            
        return duration
    except Exception:
        return 240

def parse_time_to_minutes(time_str: str) -> int:
    try:
        time_str = time_str.zfill(4)
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        return hour * 60 + minute
    except:
        return 0

def is_valid_connection(outbound_flight: dict, inbound_flight: dict, min_layover_hours: int = 1, max_layover_hours: int = 8) -> bool:
    try:
        if outbound_flight['destination'] != inbound_flight['source']:
            return False
        
        outbound_landing = parse_time_to_minutes(outbound_flight['landing'])
        inbound_takeoff = parse_time_to_minutes(inbound_flight['takeoff'])
        
        if inbound_takeoff < outbound_landing:
            layover_minutes = (24 * 60 - outbound_landing) + inbound_takeoff
        else:
            layover_minutes = inbound_takeoff - outbound_landing
        
        layover_hours = layover_minutes / 60
        return min_layover_hours <= layover_hours <= max_layover_hours
        
    except Exception:
        return False

def create_connection_flight(outbound_flight: dict, inbound_flight: dict) -> dict:
    try:
        total_cost = int(outbound_flight['cost']) + int(inbound_flight['cost'])
        
        outbound_landing = parse_time_to_minutes(outbound_flight['landing'])
        inbound_takeoff = parse_time_to_minutes(inbound_flight['takeoff'])
        
        if inbound_takeoff < outbound_landing:
            layover_minutes = (24 * 60 - outbound_landing) + inbound_takeoff
        else:
            layover_minutes = inbound_takeoff - outbound_landing
        
        total_duration = outbound_flight['duration'] + layover_minutes + inbound_flight['duration']
        layover_hours = layover_minutes / 60
        
        return {
            "year": outbound_flight['year'],
            "month": outbound_flight['month'],
            "day": outbound_flight['day'],
            "source": outbound_flight['source'],
            "destination": inbound_flight['destination'],
            "cost": str(total_cost),
            "takeoff": outbound_flight['takeoff'],
            "landing": inbound_flight['landing'],
            "duration": int(total_duration),
            "airline": f"{outbound_flight['airline']} + {inbound_flight['airline']}",  # Fixed: added airline field
            "is_connecting": True,
            "connection_airport": outbound_flight['destination'],
            "layover_hours": round(layover_hours, 1),
            "airlines": [outbound_flight['airline'], inbound_flight['airline']],
            "segments": [
                {
                    "source": outbound_flight['source'],
                    "destination": outbound_flight['destination'],
                    "takeoff": outbound_flight['takeoff'],
                    "landing": outbound_flight['landing'],
                    "duration": outbound_flight['duration'],
                    "cost": outbound_flight['cost'],
                    "airline": outbound_flight['airline']
                },
                {
                    "source": inbound_flight['source'],
                    "destination": inbound_flight['destination'],
                    "takeoff": inbound_flight['takeoff'],
                    "landing": inbound_flight['landing'],
                    "duration": inbound_flight['duration'],
                    "cost": inbound_flight['cost'],
                    "airline": inbound_flight['airline']
                }
            ]
        }
    except Exception as e:
        print(f"Error creating connection flight: {e}")
        return None

def find_connecting_flights(source: str, destination: str, year: int, month: int, day: int, priority: str = "cost", airline: str = None) -> list:
    try:
        airline_pattern = airline if airline else "$airline"
        all_flights_query = f'''!(match &space
            (flight {year} {month} {day} $src $dest $cost $takeoff $landing {airline_pattern})
            (flight {year} {month} {day} $src $dest $cost $takeoff $landing {airline_pattern}))'''
        
        all_flights_result = metta.run(all_flights_query)
        all_flights = metta_serializer(all_flights_result)
        
        if not all_flights:
            return []
        
        outbound_flights = [f for f in all_flights if f['source'] == source]
        inbound_flights = [f for f in all_flights if f['destination'] == destination]
        
        connections = []
        for outbound in outbound_flights:
            for inbound in inbound_flights:
                if is_valid_connection(outbound, inbound):
                    connection = create_connection_flight(outbound, inbound)
                    if connection:
                        connections.append(connection)
        
        return sort_flights(connections, priority)
        
    except Exception as e:
        print(f"Error finding connecting flights: {e}")
        return []

def metta_serializer(metta_result):
    result = []
    if not metta_result:
        return result
    
    data_to_process = metta_result
    if isinstance(metta_result, list) and len(metta_result) > 0:
        data_to_process = metta_result[0] if isinstance(metta_result[0], list) else metta_result
    
    for item in data_to_process:
        if isinstance(item, ExpressionAtom):
            expr = item.get_children()
            if len(expr) >= 10 and str(expr[0]) == "flight":
                airline = str(expr[9])
                duration = calculate_flight_duration(str(expr[7]), str(expr[8]))
                
                result.append({
                    "year": str(expr[1]),
                    "month": str(expr[2]),
                    "day": str(expr[3]),
                    "source": str(expr[4]),
                    "destination": str(expr[5]),
                    "cost": str(expr[6]),
                    "takeoff": str(expr[7]),
                    "landing": str(expr[8]),
                    "airline": airline if airline else "Unknown",
                    "duration": duration,
                })
        elif hasattr(item, '__str__'):
            item_str = str(item)
            if item_str.startswith("(flight "):
                parts = item_str.strip("()").split()
                if len(parts) >= 10:
                    duration = calculate_flight_duration(parts[7], parts[8])
                    
                    result.append({
                        "year": parts[1],
                        "month": parts[2],
                        "day": parts[3],
                        "source": parts[4],
                        "destination": parts[5],
                        "cost": parts[6],
                        "takeoff": parts[7],
                        "landing": parts[8],
                        "airline": parts[9],
                        "duration": duration
                    })
    
    return result

def sort_flights(flights, priority):
    """Sort flights based on priority"""
    if not flights:
        return flights
    
    try:
        if priority == "cost":
            return sorted(flights, key=lambda x: int(x.get('cost', 0)))
        elif priority == "time":
            return sorted(flights, key=lambda x: x.get('duration', 0))
        elif priority == "optimized":
            if len(flights) == 1:
                return flights
                
            min_cost = min(int(f.get('cost', 0)) for f in flights)
            max_cost = max(int(f.get('cost', 0)) for f in flights)
            min_duration = min(f.get('duration', 0) for f in flights)
            max_duration = max(f.get('duration', 0) for f in flights)
            
            cost_range = max_cost - min_cost if max_cost != min_cost else 1
            duration_range = max_duration - min_duration if max_duration != min_duration else 1
            
            def combined_score(flight):
                normalized_cost = (int(flight.get('cost', 0)) - min_cost) / cost_range
                normalized_duration = (flight.get('duration', 0) - min_duration) / duration_range
                return (normalized_cost + normalized_duration) / 2
            
            return sorted(flights, key=combined_score)
        else:
            return sorted(flights, key=lambda x: int(x.get('cost', 0)))
    except Exception as e:
        print(f"Error sorting flights: {e}")
        return flights

def search_flights(source=None, destination=None, year=None, month=None, day=None, airline=None, priority="cost"):
    src_pattern = source if source else "$src"
    dest_pattern = destination if destination else "$dest"
    year_pattern = year if year else "$year"
    month_pattern = month if month else "$month"
    day_pattern = day if day else "$day"
    airline_pattern = airline if airline else "$airline"
    
    query = f'''!(match &space 
        (flight {year_pattern} {month_pattern} {day_pattern} {src_pattern} {dest_pattern} $cost $takeoff $landing {airline_pattern}) 
        (flight {year_pattern} {month_pattern} {day_pattern} {src_pattern} {dest_pattern} $cost $takeoff $landing {airline_pattern}))'''
    
    try:
        result = metta.run(query)
        parsed_results = metta_serializer(result)
        return sort_flights(parsed_results, priority)
    except Exception as e:
        print(f"Error searching flights: {e}")
        return []

def smart_search(source=None, destination=None, year=None, month=None, day=None, airline=None, priority="cost", include_connections=True):
    try:
        direct_flights = search_flights(source=source, destination=destination, year=year, month=month, day=day, airline=airline, priority=priority)
        
        if include_connections and source and destination and year and month and day:
            connecting_flights = find_connecting_flights(source, destination, year, month, day, priority, airline)
            all_flights = direct_flights + connecting_flights
            sorted_flights = sort_flights(all_flights, priority)
        else:
            sorted_flights = direct_flights
        
        # Return only top 3 flights based on priority sorting
        return sorted_flights[:3]
    except Exception as e:
        print(f"Error in smart_search: {e}")
        return []

def get_clean_flight_data(flights):
    """Fixed version that handles both direct and connecting flights properly"""
    clean_flights = []
    
    for flight in flights:
        try:
            # Handle airline field properly for both direct and connecting flights
            if flight.get('is_connecting', False):
                # For connecting flights, use the combined airline string or list
                airlines_list = flight.get('airlines', [])
                if isinstance(airlines_list, list) and len(airlines_list) > 0:
                    airline_display = ' + '.join([str(a).replace('_', ' ') for a in airlines_list])
                else:
                    # Use the combined airline field if available
                    airline_display = str(flight.get('airline', 'Unknown')).replace('_', ' ')
            else:
                # For direct flights
                airline_display = str(flight.get('airline', 'Unknown')).replace('_', ' ')
            
            clean_flight = {
                "year": str(flight.get('year', '')),
                "month": str(flight.get('month', '')),
                "day": str(flight.get('day', '')),
                "source": str(flight.get('source', '')),
                "destination": str(flight.get('destination', '')),
                "cost": str(flight.get('cost', '0')),
                "departure": str(flight.get('takeoff', '')),
                "arrival": str(flight.get('landing', '')),
                "airline": airline_display,
                "duration_minutes": int(flight.get('duration', 0)),
                "is_connecting": bool(flight.get('is_connecting', False))
            }
            
            # Add connecting flight specific fields
            if flight.get('is_connecting'):
                clean_flight.update({
                    "connection_airport": flight.get('connection_airport'),
                    "layover_hours": flight.get('layover_hours'),
                    "airlines": [str(a).replace('_', ' ') for a in flight.get('airlines', [])],
                    "segments": flight.get('segments', [])
                })
                
            clean_flights.append(clean_flight)
            
        except Exception as e:
            print(f"Error processing flight data: {e}")
            continue
    
    return clean_flights

# API Endpoints


@app.post("/api/users/authenticate")
async def authenticate_user(credentials: Credentials):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND mpin = ?", (credentials.username, credentials.mpin))
        user = cursor.fetchone()
        conn.close()

        if user:
            return {"success": True, "message": "Authentication successful."}
        else:
            return {"success": False, "message": "Invalid username or MPIN."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/api/bookings/create")
async def create_booking(booking: BookingRequest):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        # Convert flight details to a JSON string for storage
        import json
        flight_details_json = json.dumps(booking.flight_details)
        booking_date = datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO bookings (username, flight_details, booking_date) VALUES (?, ?, ?)",
            (booking.username, flight_details_json, booking_date)
        )
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()

        if booking_id:
            return {"success": True, "message": "Booking created successfully.", "booking_id": booking_id}
        else:
            return {"success": False, "message": "Booking failed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/flights/search", response_model=FlightSearchResponse, tags=["Flight Search"])
async def search_flights_get(
    source: Optional[str] = Query(None, description="Source airport code"),
    destination: Optional[str] = Query(None, description="Destination airport code"),
    year: Optional[int] = Query(None, description="Year"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Month (1-12)"),
    day: Optional[int] = Query(None, ge=1, le=31, description="Day (1-31)"),
    airline: Optional[str] = Query(None, description="Airline name"),
    priority: str = Query("cost", description="Sort priority: cost, time, or optimized"),
    include_connections: bool = Query(True, description="Include connecting flights")
):
    """
    Search for flights using GET request with query parameters.
    """
    try:
        # Validate priority
        if priority not in ['cost', 'time', 'optimized']:
            raise HTTPException(status_code=400, detail="Priority must be 'cost', 'time', or 'optimized'")
        
        # Search flights
        flights = smart_search(
            source=source,
            destination=destination,
            year=year,
            month=month,
            day=day,
            airline=airline,
            priority=priority,
            include_connections=include_connections
        )
        
        # Get clean data
        clean_data = get_clean_flight_data(flights)
        
        return FlightSearchResponse(
            success=True,
            count=len(clean_data),
            flights=clean_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/airlines", response_model=AirlinesResponse, tags=["Reference Data"])
async def get_airlines():
    """Get all available airlines."""
    try:
        query = '''!(match &space (flight $year $month $day $src $dest $cost $takeoff $landing $airline) $airline)'''
        result = metta.run(query)
        
        airlines = set()
        if result and isinstance(result, list):
            data_to_process = result[0] if isinstance(result[0], list) else result
            for item in data_to_process:
                airline = str(item).replace('_', ' ')
                airlines.add(airline)
        
        return AirlinesResponse(
            success=True,
            airlines=sorted(list(airlines))
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/airports", response_model=AirportsResponse, tags=["Reference Data"])
async def get_airports():
    """Get all available airports."""
    try:
        query = '''!(match &space (flight $year $month $day $src $dest $cost $takeoff $landing $airline) ($src $dest))'''
        result = metta.run(query)
        
        airports = set()
        if result and isinstance(result, list):
            data_to_process = result[0] if isinstance(result[0], list) else result
            for item in data_to_process:
                if isinstance(item, ExpressionAtom):
                    children = item.get_children()
                    if len(children) >= 2:
                        airports.add(str(children[0]))
                        airports.add(str(children[1]))
                else:
                    # Handle string representation
                    item_str = str(item).strip("()")
                    if " " in item_str:
                        parts = item_str.split()
                        if len(parts) >= 2:
                            airports.add(parts[0])
                            airports.add(parts[1])
        
        return AirportsResponse(
            success=True,
            airports=sorted(list(airports))
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", 
        message="Flight Search API is running"
    )
# In your FastAPI api.py file

@app.get("/api/users/check_existence")
async def check_user_existence(username: str):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone() is not None
        conn.close()

        return {"exists": user_exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/", tags=["Documentation"])
async def root():
    """
    API root endpoint with basic information.
    Visit /docs for Swagger UI or /redoc for ReDoc documentation.
    """
    return {
        "message": "Flight Search FastAPI",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "search_flights": "/api/flights/search",
            "get_airlines": "/api/airlines",
            "get_airports": "/api/airports",
            "health_check": "/api/health"
        }
    }

# Initialize dataset on startup
@app.on_event("startup")
async def startup_event():
    try:
        load_dataset("flights.metta")
        print("Flight data loaded successfully!")
    except Exception as e:
        print(f"Error loading dataset: {e}")

# Run with: uvicorn flight_fastapi:app --reload --host 0.0.0.0 --port 8003
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)