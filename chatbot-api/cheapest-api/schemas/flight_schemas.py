from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PriorityType(str, Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    OPTIMIZED = "optimized"

class CabinClass(str, Enum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"

class FlightSearchRequest(BaseModel):
    source: str = Field(..., description="Source airport code (e.g., JFK)")
    destination: str = Field(..., description="Destination airport code (e.g., LAX)")
    year: int = Field(..., description="Year of travel")
    month: int = Field(..., description="Month of travel (1-12)")
    day: int = Field(..., description="Day of travel (1-31)")
    passengers: int = Field(default=1, description="Number of passengers")
    cabin_class: CabinClass = Field(default=CabinClass.ECONOMY, description="Cabin class preference")
    include_connections: bool = Field(default=True, description="Include connecting flights")
    max_connections: int = Field(default=2, description="Maximum number of connections")

class AirlineInfo(BaseModel):
    code: str = Field(..., description="Airline code (e.g., AA)")
    name: str = Field(..., description="Airline name")
    logo: Optional[str] = Field(None, description="Airline logo URL")
    description: Optional[str] = Field(None, description="Airline description")

class FlightSegment(BaseModel):
    """Individual flight segment for multi-stop flights"""
    segment_id: str = Field(..., description="Unique segment identifier")
    flight_number: str = Field(..., description="Flight number")
    departure_airport: str = Field(..., description="Departure airport code")
    arrival_airport: str = Field(..., description="Arrival airport code")
    departure_time: str = Field(..., description="Departure time (HH:MM)")
    arrival_time: str = Field(..., description="Arrival time (HH:MM)")
    duration_minutes: int = Field(..., description="Flight duration in minutes")
    aircraft: Optional[str] = Field(None, description="Aircraft type")
    airline: AirlineInfo = Field(..., description="Airline information")

class PassengerInfo(BaseModel):
    """Passenger information for booking"""
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Email address")
    date_of_birth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    passport_number: Optional[str] = Field(None, description="Passport number")
    nationality: str = Field(..., description="Nationality")
    seat_preference: Optional[str] = Field(None, description="Seat preference (window/aisle)")
    meal_preference: Optional[str] = Field(None, description="Meal preference")

class FlightDetails(BaseModel):
    """Complete flight details for booking"""
    # Basic flight information
    id: str = Field(..., description="Unique flight identifier")
    source: str = Field(..., description="Source airport code")
    destination: str = Field(..., description="Destination airport code")
    year: int = Field(..., description="Year of travel")
    month: int = Field(..., description="Month of travel")
    day: int = Field(..., description="Day of travel")
    
    # Timing information
    departure_time: str = Field(..., description="Departure time")
    arrival_time: str = Field(..., description="Arrival time")
    duration: str = Field(..., description="Total duration (e.g., '2h 30m')")
    duration_minutes: int = Field(..., description="Duration in minutes")
    
    # Cost and pricing
    cost: float = Field(..., description="Flight cost in USD")
    currency: str = Field(default="USD", description="Currency code")
    base_fare: float = Field(..., description="Base fare")
    taxes: float = Field(..., description="Taxes and fees")
    total_fare: float = Field(..., description="Total fare including taxes")
    
    # Airline information
    airline: AirlineInfo = Field(..., description="Airline details")
    flight_number: str = Field(..., description="Flight number")
    
    # Route information
    stops: int = Field(..., description="Number of stops")
    is_connecting: bool = Field(..., description="Is this a connecting flight")
    connection_airport: Optional[str] = Field(None, description="Connection airport code")
    layover_hours: float = Field(default=0, description="Layover duration in hours")
    
    # Flight segments for multi-stop flights (optional to handle different API formats)
    segments: Optional[List[FlightSegment]] = Field(default=None, description="Individual flight segments")
    
    # Aircraft and cabin information
    aircraft: str = Field(default="Boeing 737", description="Aircraft type")
    cabin_class: CabinClass = Field(default=CabinClass.ECONOMY, description="Cabin class")
    
    # Booking details
    available_seats: int = Field(..., description="Number of available seats")
    seat_class: str = Field(default="Economy", description="Seat class")
    baggage_allowance: Dict[str, Any] = Field(default_factory=dict, description="Baggage allowance details")
    refund_policy: str = Field(default="Non-refundable", description="Refund policy")
    change_policy: str = Field(default="Change fee applies", description="Change policy")
    
    # Additional services
    meal_included: bool = Field(default=True, description="Meal included")
    entertainment: bool = Field(default=True, description="Entertainment available")
    wifi_available: bool = Field(default=False, description="WiFi available")
    power_outlets: bool = Field(default=True, description="Power outlets available")
    
    # Booking metadata
    booking_class: str = Field(..., description="Booking class code")
    fare_basis: str = Field(..., description="Fare basis code")
    ticket_type: str = Field(default="Electronic", description="Ticket type")
    
    # Timestamps
    search_timestamp: datetime = Field(default_factory=datetime.now, description="When this flight was searched")
    valid_until: datetime = Field(..., description="When this fare expires")
    
    # User information
    passenger_info: Optional[PassengerInfo] = Field(None, description="Current user passenger information")

class ContactInfo(BaseModel):
    """Contact information for booking"""
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    address: str = Field(..., description="Address")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")
    postal_code: str = Field(..., description="Postal code")

class ContactInfo(BaseModel):
    """Contact information for booking"""
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    address: str = Field(..., description="Address")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")
    postal_code: str = Field(..., description="Postal code")

class PaymentInfo(BaseModel):
    """Payment information for booking"""
    card_type: str = Field(..., description="Card type (Visa/MasterCard/etc.)")
    card_number: str = Field(..., description="Card number (masked)")
    expiry_date: str = Field(..., description="Expiry date (MM/YY)")
    cvv: str = Field(..., description="CVV code")
    cardholder_name: str = Field(..., description="Cardholder name")
    billing_address: str = Field(..., description="Billing address")

class FlightSearchResponse(BaseModel):
    """Unified response for all flight search APIs"""
    success: bool = Field(..., description="Whether the search was successful")
    message: str = Field(..., description="Response message")
    
    # Flight details
    flight: Optional[FlightDetails] = Field(None, description="Flight details")
    
    # Search metadata
    total_flights: int = Field(default=0, description="Total flights found")
    search_time_ms: float = Field(..., description="Search time in milliseconds")
    priority_type: PriorityType = Field(..., description="Search priority type")
    
    # Request details
    source: str = Field(..., description="Source airport")
    destination: str = Field(..., description="Destination airport")
    search_date: str = Field(..., description="Search date (YYYY-MM-DD)")
    
    # Additional information
    alternative_flights: List[FlightDetails] = Field(default=[], description="Alternative flight options")
    price_history: Optional[Dict[str, Any]] = Field(None, description="Price history data")
    recommendations: Optional[List[str]] = Field(None, description="Travel recommendations")

class BookingRequest(BaseModel):
    """Complete booking request"""
    flight_id: str = Field(..., description="Flight ID to book")
    passengers: List[PassengerInfo] = Field(..., description="Passenger information")
    contact_info: ContactInfo = Field(..., description="Contact information")
    payment_info: PaymentInfo = Field(..., description="Payment information")
    special_requests: Optional[str] = Field(None, description="Special requests")
    insurance: bool = Field(default=False, description="Travel insurance required")

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