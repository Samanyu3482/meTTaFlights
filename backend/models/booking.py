from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_ref = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="confirmed")  # confirmed, cancelled, completed
    
    # Flight details
    flight_year = Column(String(4), nullable=False)
    flight_month = Column(String(2), nullable=False)
    flight_day = Column(String(2), nullable=False)
    source = Column(String(10), nullable=False)
    destination = Column(String(10), nullable=False)
    cost = Column(String(20), nullable=False)
    takeoff = Column(String(4), nullable=False)
    landing = Column(String(4), nullable=False)
    duration = Column(Integer, nullable=False)
    
    # Airline details
    airline_code = Column(String(10), nullable=True)
    airline_name = Column(String(100), nullable=True)
    airline_logo = Column(String(255), nullable=True)
    airline_description = Column(Text, nullable=True)
    
    # Flight type
    is_connecting = Column(Boolean, default=False)
    connection_airport = Column(String(10), nullable=True)
    layover_hours = Column(Float, nullable=True)
    
    # Booking details
    total_cost = Column(Float, nullable=False)
    passenger_count = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    passengers = relationship("Passenger", back_populates="booking", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")

class Passenger(Base):
    __tablename__ = "passengers"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(String(10), nullable=False)
    passport_number = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    seat_preference = Column(String(20), default="window")
    special_requests = Column(Text, nullable=True)
    
    # Relationships
    booking = relationship("Booking", back_populates="passengers")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    card_number = Column(String(20), nullable=False)  # Last 4 digits only
    card_holder_name = Column(String(100), nullable=False)
    expiry_month = Column(String(2), nullable=False)
    expiry_year = Column(String(4), nullable=False)
    cvv = Column(String(4), nullable=False)
    billing_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    
    # Relationships
    booking = relationship("Booking", back_populates="payment") 