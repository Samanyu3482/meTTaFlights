from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from main import load_dataset, smart_search, search_all_flights

app = FastAPI(title="MeTTa Flight Search API", version="1.0.0")

# Add CORS middleware to allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
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

class FlightSearchRequest(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None

class FlightResponse(BaseModel):
    year: str
    month: str
    day: str
    source: str
    destination: str
    cost: str

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
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/all", response_model=List[FlightResponse])
def get_all_flights():
    """
    Get all flights from the knowledge base
    """
    try:
        results = search_all_flights()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching flights: {str(e)}")

@app.get("/api/flights/source/{source}", response_model=List[FlightResponse])
def search_by_source_airport(source: str):
    """
    Search flights by source airport
    """
    try:
        results = smart_search(source=source.upper())
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/destination/{destination}", response_model=List[FlightResponse])
def search_by_destination_airport(destination: str):
    """
    Search flights by destination airport
    """
    try:
        results = smart_search(destination=destination.upper())
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/flights/route/{source}/{destination}", response_model=List[FlightResponse])
def search_by_route(source: str, destination: str):
    """
    Search flights by source and destination
    """
    try:
        results = smart_search(source=source.upper(), destination=destination.upper())
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 