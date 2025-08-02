#!/usr/bin/env python3
"""
Unified Booking API
Integrates with the three flight search APIs and the existing booking system
"""

import asyncio
import json
import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import jwt
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="Unified Booking API",
    description="API to book flights from search results and integrate with booking system",
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

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
security = HTTPBearer()

# API Configuration
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8001")
CHEAPEST_API_URL = os.getenv("CHEAPEST_API_URL", "http://localhost:8001")
FASTEST_API_URL = os.getenv("FASTEST_API_URL", "http://localhost:8003")
OPTIMIZED_API_URL = os.getenv("OPTIMIZED_API_URL", "http://localhost:8002")

# Schemas
class PriorityType(str, Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    OPTIMIZED = "optimized"

class AirlineInfo(BaseModel):
    code: str = Field(..., description="Airline code (e.g., AA)")
    name: str = Field(..., description="Airline name")
    logo: Optional[str] = Field(None, description="Airline logo URL")
    description: Optional[str] = Field(None, description="Airline description")

class FlightDetails(BaseModel):
    """Flight details from search APIs"""
    id: str = Field(..., description="Unique flight identifier")
    source: str = Field(..., description="Source airport code")
    destination: str = Field(..., description="Destination airport code")
    year: int = Field(..., description="Year of travel")
    month: int = Field(..., description="Month of travel")
    day: int = Field(..., description="Day of travel")
    departure_time: str = Field(..., description="Departure time")
    arrival_time: str = Field(..., description="Arrival time")
    duration: str = Field(..., description="Total duration")
    duration_minutes: int = Field(..., description="Duration in minutes")
    cost: float = Field(..., description="Flight cost in USD")
    currency: str = Field(default="USD", description="Currency code")
    airline: AirlineInfo = Field(..., description="Airline details")
    flight_number: str = Field(..., description="Flight number")
    stops: int = Field(..., description="Number of stops")
    is_connecting: bool = Field(..., description="Is this a connecting flight")
    connection_airport: Optional[str] = Field(None, description="Connection airport code")
    layover_hours: float = Field(default=0, description="Layover duration in hours")

class PassengerInfo(BaseModel):
    """Passenger information for booking"""
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Email address")
    date_of_birth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    passport_number: str = Field(..., description="Passport number")
    phone: str = Field(..., description="Phone number")
    seat_preference: str = Field(default="window", description="Seat preference")
    special_requests: Optional[str] = Field(None, description="Special requests")

class PaymentInfo(BaseModel):
    """Payment information for booking"""
    card_number: str = Field(..., description="Card number")
    card_holder_name: str = Field(..., description="Cardholder name")
    expiry_month: str = Field(..., description="Expiry month (MM)")
    expiry_year: str = Field(..., description="Expiry year (YYYY)")
    cvv: str = Field(..., description="CVV code")
    billing_address: str = Field(..., description="Billing address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="ZIP code")
    country: str = Field(default="United States", description="Country")

class UnifiedBookingRequest(BaseModel):
    """Unified booking request that accepts flight details from any search API"""
    flight_details: FlightDetails = Field(..., description="Flight details from search API")
    passengers: List[PassengerInfo] = Field(..., description="Passenger information")
    payment: PaymentInfo = Field(..., description="Payment information")
    search_priority: PriorityType = Field(..., description="Which search API was used")
    search_api_response: Optional[Dict[str, Any]] = Field(None, description="Original search API response")

class BookingResponse(BaseModel):
    """Booking confirmation response"""
    success: bool = Field(..., description="Whether booking was successful")
    booking_reference: str = Field(..., description="Booking reference number")
    message: str = Field(..., description="Booking message")
    flight_details: FlightDetails = Field(..., description="Confirmed flight details")
    total_amount: float = Field(..., description="Total booking amount")
    currency: str = Field(default="USD", description="Currency")
    booking_timestamp: datetime = Field(default_factory=datetime.now, description="Booking timestamp")
    e_ticket_number: Optional[str] = Field(None, description="E-ticket number")
    terms_and_conditions: str = Field(..., description="Terms and conditions")

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

def convert_flight_details_to_backend_format(flight_details: FlightDetails) -> Dict[str, Any]:
    """Convert flight details from search API format to backend booking format"""
    return {
        "year": str(flight_details.year),
        "month": str(flight_details.month),
        "day": str(flight_details.day),
        "source": flight_details.source,
        "destination": flight_details.destination,
        "cost": f"${flight_details.cost:,.2f}",
        "takeoff": flight_details.departure_time,
        "landing": flight_details.arrival_time,
        "duration": flight_details.duration_minutes,
        "is_connecting": flight_details.is_connecting,
        "connection_airport": flight_details.connection_airport,
        "layover_hours": flight_details.layover_hours,
        "airline": {
            "code": flight_details.airline.code,
            "name": flight_details.airline.name,
            "logo": flight_details.airline.logo,
            "description": flight_details.airline.description
        }
    }

def convert_passenger_to_backend_format(passenger: PassengerInfo) -> Dict[str, Any]:
    """Convert passenger info to backend format"""
    return {
        "first_name": passenger.first_name,
        "last_name": passenger.last_name,
        "date_of_birth": passenger.date_of_birth,
        "passport_number": passenger.passport_number,
        "email": passenger.email,
        "phone": passenger.phone,
        "seat_preference": passenger.seat_preference,
        "special_requests": passenger.special_requests
    }

def convert_payment_to_backend_format(payment: PaymentInfo) -> Dict[str, Any]:
    """Convert payment info to backend format"""
    return {
        "card_number": payment.card_number,
        "card_holder_name": payment.card_holder_name,
        "expiry_month": payment.expiry_month,
        "expiry_year": payment.expiry_year,
        "cvv": payment.cvv,
        "billing_address": payment.billing_address,
        "city": payment.city,
        "state": payment.state,
        "zip_code": payment.zip_code,
        "country": payment.country
    }

@app.get("/api/unified-booking/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Unified Booking API",
        "timestamp": datetime.now().isoformat(),
        "integrated_apis": {
            "backend_api": BACKEND_API_URL,
            "cheapest_api": CHEAPEST_API_URL,
            "fastest_api": FASTEST_API_URL,
            "optimized_api": OPTIMIZED_API_URL
        }
    }

@app.post("/api/unified-booking/book-flight")
async def book_flight(
    request: UnifiedBookingRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Book a flight using details from any of the three search APIs
    """
    start_time = datetime.now()
    
    try:
        # Convert flight details to backend format
        backend_flight_data = convert_flight_details_to_backend_format(request.flight_details)
        
        # Convert passengers to backend format
        backend_passengers = [convert_passenger_to_backend_format(p) for p in request.passengers]
        
        # Convert payment to backend format
        backend_payment = convert_payment_to_backend_format(request.payment)
        
        # Prepare booking request for backend
        booking_request = {
            "flight": backend_flight_data,
            "passengers": backend_passengers,
            "payment": backend_payment,
            "passenger_count": len(request.passengers)
        }
        
        # Make booking request to backend API
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {current_user['token']}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                f"{BACKEND_API_URL}/api/bookings",
                json=booking_request,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Backend booking failed: {response.text}"
                )
            
            booking_response = response.json()
            
            # Calculate total amount
            total_amount = request.flight_details.cost * len(request.passengers)
            
            # Generate e-ticket number
            e_ticket_number = f"ET{datetime.now().strftime('%Y%m%d%H%M%S')}{current_user['user_id']}"
            
            # Prepare unified response
            unified_response = BookingResponse(
                success=True,
                booking_reference=booking_response.get("booking_ref", "N/A"),
                message="Flight booked successfully! Your booking has been added to your trips.",
                flight_details=request.flight_details,
                total_amount=total_amount,
                currency=request.flight_details.currency,
                booking_timestamp=datetime.now(),
                e_ticket_number=e_ticket_number,
                terms_and_conditions="Standard airline terms and conditions apply. Changes and cancellations subject to airline policies."
            )
            
            search_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": True,
                "message": "Flight booked successfully",
                "booking": unified_response.dict(),
                "search_time_ms": search_time,
                "search_priority": request.search_priority,
                "user_id": current_user["user_id"]
            }
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Backend service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Booking failed: {str(e)}"
        )

@app.get("/api/unified-booking/user-bookings")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    """Get all bookings for the current user"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {current_user['token']}",
                "Content-Type": "application/json"
            }
            
            response = await client.get(
                f"{BACKEND_API_URL}/api/bookings",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch bookings: {response.text}"
                )
            
            return response.json()
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Backend service unavailable: {str(e)}"
        )

@app.get("/api/unified-booking/booking/{booking_ref}")
async def get_booking_details(
    booking_ref: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific booking details"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {current_user['token']}",
                "Content-Type": "application/json"
            }
            
            response = await client.get(
                f"{BACKEND_API_URL}/api/bookings/{booking_ref}",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch booking: {response.text}"
                )
            
            return response.json()
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Backend service unavailable: {str(e)}"
        )

@app.delete("/api/unified-booking/booking/{booking_ref}")
async def cancel_booking(
    booking_ref: str,
    current_user: dict = Depends(get_current_user)
):
    """Cancel a booking"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {current_user['token']}",
                "Content-Type": "application/json"
            }
            
            response = await client.delete(
                f"{BACKEND_API_URL}/api/bookings/{booking_ref}",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to cancel booking: {response.text}"
                )
            
            return response.json()
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Backend service unavailable: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005) 