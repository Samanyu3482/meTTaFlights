from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# User schemas
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip() if v else v

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MessageResponse(BaseModel):
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# Search history schemas
class SearchHistoryRequest(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    passengers: int = 1
    travel_class: str = "economy"

class SearchHistoryResponse(BaseModel):
    id: int
    source: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    passengers: int
    travel_class: str
    created_at: datetime

    class Config:
        from_attributes = True

# Favorite routes schemas
class FavoriteRouteRequest(BaseModel):
    source: str
    destination: str
    route_name: Optional[str] = None

class FavoriteRouteResponse(BaseModel):
    id: int
    source: str
    destination: str
    route_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Saved passengers schemas
class SavedPassengerRequest(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    passport_number: str
    email: str
    phone: str
    seat_preference: str = "window"
    special_requests: Optional[str] = None
    is_primary: bool = False

class SavedPassengerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: str
    passport_number: str
    email: str
    phone: str
    seat_preference: str
    special_requests: Optional[str] = None
    is_primary: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Saved payments schemas
class SavedPaymentRequest(BaseModel):
    card_number: str
    card_holder_name: str
    expiry_month: str
    expiry_year: str
    billing_address: str
    city: str
    state: str
    zip_code: str
    country: str
    is_default: bool = False

class SavedPaymentResponse(BaseModel):
    id: int
    card_number: str  # Last 4 digits only
    card_holder_name: str
    expiry_month: str
    expiry_year: str
    billing_address: str
    city: str
    state: str
    zip_code: str
    country: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True