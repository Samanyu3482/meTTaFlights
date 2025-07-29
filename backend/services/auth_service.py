import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.user import User, UserSession
import os
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "meTTaFlights-super-secret-jwt-key-2024-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    def register_user(self, db: Session, email: str, password: str, name: str) -> Optional[User]:
        """Register a new user"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return None
        
        # Hash password and create user
        hashed_password = self.hash_password(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            name=name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        return user
    
    def create_user_session(self, db: Session, user_id: int, token: str) -> UserSession:
        """Create a user session with token"""
        session = UserSession(
            user_id=user_id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def update_user_profile(self, db: Session, user_id: int, profile_data: dict) -> Optional[User]:
        """Update user profile information"""
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None
        
        # Update allowed fields
        allowed_fields = ['name', 'phone', 'date_of_birth', 'nationality', 'address', 'emergency_contact']
        for field in allowed_fields:
            if field in profile_data:
                setattr(user, field, profile_data[field])
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    def invalidate_user_sessions(self, db: Session, user_id: int) -> bool:
        """Invalidate all sessions for a user (logout)"""
        sessions = db.query(UserSession).filter(UserSession.user_id == user_id).all()
        for session in sessions:
            db.delete(session)
        db.commit()
        return True
    
    def cleanup_expired_sessions(self, db: Session) -> int:
        """Clean up expired sessions"""
        expired_sessions = db.query(UserSession).filter(UserSession.expires_at < datetime.utcnow()).all()
        count = len(expired_sessions)
        for session in expired_sessions:
            db.delete(session)
        db.commit()
        return count

# Create global instance
auth_service = AuthService()