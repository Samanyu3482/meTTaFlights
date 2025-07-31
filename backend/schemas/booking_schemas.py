from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

# Passenger schemas
class PassengerInfo(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    passport_number: str
    email: str
    phone: str
    seat_preference: str = "window"
    special_requests: Optional[str] = None

# Payment schemas
class PaymentInfo(BaseModel):
    card_number: str
    card_holder_name: str
    expiry_month: str
    expiry_year: str
    cvv: str
    billing_address: str
    city: str
    state: str
    zip_code: str
    country: str = "United States"

# Flight details schema
class FlightDetails(BaseModel):
    year: str
    month: str
    day: str
    source: str
    destination: str
    cost: str
    takeoff: str
    landing: str
    duration: int
    is_connecting: Optional[bool] = False
    connection_airport: Optional[str] = None
    layover_hours: Optional[float] = None
    airline: Optional[dict] = None

# Booking request schema
class CreateBookingRequest(BaseModel):
    flight: FlightDetails
    passengers: List[PassengerInfo]
    payment: PaymentInfo
    passenger_count: int

# Booking response schemas
class PassengerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: str
    passport_number: str
    email: str
    phone: str
    seat_preference: str
    special_requests: Optional[str] = None

    class Config:
        from_attributes = True

class PaymentResponse(BaseModel):
    id: int
    card_number: str  # Last 4 digits only
    card_holder_name: str
    expiry_month: str
    expiry_year: str
    cvv: str
    billing_address: str
    city: str
    state: str
    zip_code: str
    country: str

    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    id: int
    booking_ref: str
    status: str
    user_id: int
    
    # Flight details
    flight_year: str
    flight_month: str
    flight_day: str
    source: str
    destination: str
    cost: str
    takeoff: str
    landing: str
    duration: int
    
    # Airline details
    airline_code: Optional[str] = None
    airline_name: Optional[str] = None
    airline_logo: Optional[str] = None
    airline_description: Optional[str] = None
    
    # Flight type
    is_connecting: bool = False
    connection_airport: Optional[str] = None
    layover_hours: Optional[float] = None
    
    # Booking details
    total_cost: float
    passenger_count: int
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Related data
    passengers: List[PassengerResponse]
    payment: PaymentResponse

    class Config:
        from_attributes = True

# Booking update schema
class UpdateBookingStatusRequest(BaseModel):
    status: str
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['confirmed', 'cancelled', 'completed']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v

# Booking list response
class BookingListResponse(BaseModel):
    bookings: List[BookingResponse]
    total: int
    page: int
    per_page: int 