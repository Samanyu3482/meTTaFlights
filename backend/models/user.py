from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(String(10), nullable=True)
    nationality = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    source = Column(String(10), nullable=True)
    destination = Column(String(10), nullable=True)
    departure_date = Column(String(10), nullable=True)
    return_date = Column(String(10), nullable=True)
    passengers = Column(Integer, default=1)
    travel_class = Column(String(50), default="economy")
    created_at = Column(DateTime, default=func.now())

class FavoriteRoute(Base):
    __tablename__ = "favorite_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    source = Column(String(10), nullable=False)
    destination = Column(String(10), nullable=False)
    route_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())