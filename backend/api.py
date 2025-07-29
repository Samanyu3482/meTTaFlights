from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import our modules
from database.database import get_db, create_tables
from models.user import User, UserSession, SearchHistory, FavoriteRoute
from schemas.auth_schemas import (
    UserRegisterRequest, UserLoginRequest, UserProfileUpdateRequest,
    UserResponse, AuthResponse, TokenResponse, MessageResponse,
    SearchHistoryRequest, SearchHistoryResponse,
    FavoriteRouteRequest, FavoriteRouteResponse
)
from services.auth_service import auth_service
from services.dependencies import get_current_user, get_current_user_optional

load_dotenv()

app = FastAPI(
    title="meTTaFlights Authentication API",
    description="Authentication and user management API for meTTaFlights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
create_tables()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "meTTaFlights Authentication API is running"}

# Authentication endpoints
@app.post("/api/auth/register", response_model=AuthResponse)
async def register(user_data: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = auth_service.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Register the user
        user = auth_service.register_user(
            db, 
            email=user_data.email, 
            password=user_data.password, 
            name=user_data.name
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Create tokens
        access_token = auth_service.create_access_token(data={"sub": str(user.id)})
        refresh_token = auth_service.create_refresh_token(data={"sub": str(user.id)})
        
        # Create session
        auth_service.create_user_session(db, user.id, refresh_token)
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/api/auth/login", response_model=AuthResponse)
async def login(user_data: UserLoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    try:
        # Authenticate user
        user = auth_service.authenticate_user(db, user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )
        
        # Create tokens
        access_token = auth_service.create_access_token(data={"sub": str(user.id)})
        refresh_token = auth_service.create_refresh_token(data={"sub": str(user.id)})
        
        # Create session
        auth_service.create_user_session(db, user.id, refresh_token)
        
        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.post("/api/auth/refresh", response_model=TokenResponse)
async def refresh_token(request: dict, db: Session = Depends(get_db)):
    """Refresh access token"""
    try:
        refresh_token = request.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )
        
        # Verify refresh token
        payload = auth_service.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Check if session exists
        session = db.query(UserSession).filter(
            UserSession.user_id == int(user_id),
            UserSession.token == refresh_token
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found"
            )
        
        # Create new access token
        access_token = auth_service.create_access_token(data={"sub": str(user_id)})
        
        return TokenResponse(access_token=access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@app.post("/api/auth/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user"""
    try:
        auth_service.invalidate_user_sessions(db, current_user.id)
        return MessageResponse(message="Successfully logged out")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)

@app.put("/api/auth/profile", response_model=UserResponse)
async def update_profile(
    profile_data: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    try:
        updated_user = auth_service.update_user_profile(
            db, 
            current_user.id, 
            profile_data.dict(exclude_unset=True)
        )
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.from_orm(updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )

# User-specific endpoints
@app.get("/api/user/search-history", response_model=list[SearchHistoryResponse])
async def get_search_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's search history"""
    try:
        history = db.query(SearchHistory).filter(
            SearchHistory.user_id == current_user.id
        ).order_by(SearchHistory.created_at.desc()).all()
        
        return [SearchHistoryResponse.from_orm(item) for item in history]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get search history: {str(e)}"
        )

@app.post("/api/user/search-history", response_model=SearchHistoryResponse)
async def add_search_history(
    search_data: SearchHistoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a search history entry"""
    try:
        search_history = SearchHistory(
            user_id=current_user.id,
            source=search_data.source,
            destination=search_data.destination,
            departure_date=search_data.departure_date,
            return_date=search_data.return_date,
            passengers=search_data.passengers,
            travel_class=search_data.travel_class
        )
        
        db.add(search_history)
        db.commit()
        db.refresh(search_history)
        
        return SearchHistoryResponse.from_orm(search_history)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add search history: {str(e)}"
        )

# Favorite routes endpoints
@app.post("/api/user/favorite-routes", response_model=FavoriteRouteResponse)
async def add_favorite_route(
    route_data: FavoriteRouteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a favorite route"""
    try:
        favorite_route = FavoriteRoute(
            user_id=current_user.id,
            source=route_data.source,
            destination=route_data.destination,
            route_name=route_data.route_name
        )
        
        db.add(favorite_route)
        db.commit()
        db.refresh(favorite_route)
        
        return FavoriteRouteResponse.from_orm(favorite_route)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add favorite route: {str(e)}"
        )

@app.get("/api/user/favorite-routes", response_model=list[FavoriteRouteResponse])
async def get_favorite_routes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's favorite routes"""
    try:
        routes = db.query(FavoriteRoute).filter(
            FavoriteRoute.user_id == current_user.id
        ).order_by(FavoriteRoute.created_at.desc()).all()
        
        return [FavoriteRouteResponse.from_orm(route) for route in routes]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get favorite routes: {str(e)}"
        )

@app.delete("/api/user/favorite-routes/{route_id}", response_model=MessageResponse)
async def delete_favorite_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a favorite route"""
    try:
        route = db.query(FavoriteRoute).filter(
            FavoriteRoute.id == route_id,
            FavoriteRoute.user_id == current_user.id
        ).first()
        
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite route not found"
            )
        
        db.delete(route)
        db.commit()
        
        return MessageResponse(message="Favorite route deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete favorite route: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)