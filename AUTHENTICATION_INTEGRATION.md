# Authentication Integration Guide

## Overview

The MeTTa Flight Search System now includes a complete authentication system that allows users to register, login, manage their profiles, and maintain secure sessions. The authentication is implemented as a separate backend service that works alongside the existing MeTTa flight search backend.

## Architecture

```
Frontend (Next.js) ←→ Authentication Backend (FastAPI) ←→ SQLite Database
     Port 3000           Port 8001                        auth_database.db
                ←→ Flight Search Backend (FastAPI) ←→ MeTTa Knowledge Base
                        Port 8000                        flights.metta
```

## Features Implemented

### ✅ User Authentication
- **User Registration**: Create new accounts with email, password, and name
- **User Login**: Secure authentication with JWT tokens
- **User Logout**: Secure session termination
- **Password Hashing**: Bcrypt encryption for security
- **JWT Tokens**: Access and refresh token system

### ✅ User Management
- **Profile Management**: Update personal information
- **Session Management**: Track and manage user sessions
- **Account Status**: Active/inactive account states
- **Email Verification**: Support for email verification (backend ready)

### ✅ Security Features
- **JWT Authentication**: Secure token-based authentication
- **Password Security**: Bcrypt hashing with salt
- **Session Management**: Secure session handling
- **CORS Protection**: Cross-origin request security
- **Input Validation**: Pydantic schema validation

### ✅ Frontend Integration
- **Real-time Authentication**: Live authentication state
- **Protected Routes**: Profile and user-specific pages
- **User Interface**: Beautiful login/register forms
- **Profile Management**: Complete profile editing interface
- **Navigation Integration**: User-aware navigation

## Backend Services

### Authentication Backend (Port 8001)

**API Endpoints:**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/profile` - Update user profile
- `GET /api/user/search-history` - Get user search history
- `POST /api/user/search-history` - Add search history
- `GET /api/user/favorite-routes` - Get favorite routes
- `POST /api/user/favorite-routes` - Add favorite route
- `DELETE /api/user/favorite-routes/{id}` - Remove favorite route

**Database Schema:**
- `users` - User accounts and profiles
- `user_sessions` - Active user sessions
- `search_history` - User search history
- `favorite_routes` - User favorite routes

### Flight Search Backend (Port 8000)

**Remains unchanged** - All existing MeTTa flight search functionality continues to work as before.

## Frontend Integration

### Authentication Provider

The frontend uses a React Context provider (`AuthProvider`) that:
- Manages authentication state
- Handles login/logout operations
- Stores JWT tokens securely
- Provides user information to components
- Handles token refresh automatically

### Updated Components

1. **Login Page** (`/login`)
   - Real authentication with backend
   - Error handling and validation
   - Redirect to home after login

2. **Register Page** (`/register`)
   - User registration with validation
   - Password confirmation
   - Terms acceptance

3. **Profile Page** (`/profile`)
   - Real user data from backend
   - Profile editing capabilities
   - Membership tier display
   - Account information

4. **Navigation Component**
   - User-aware navigation
   - Logout functionality
   - User avatar and menu

## Getting Started

### 1. Start the System

```bash
# Make the startup script executable
chmod +x start.sh

# Start all services
./start.sh
```

This will start:
- Flight Search Backend on port 8000
- Authentication Backend on port 8001
- Next.js Frontend on port 3000

### 2. Test the Integration

```bash
# Run the integration test
python test_auth_integration.py
```

### 3. Use the Application

1. **Visit the frontend**: http://localhost:3000
2. **Register a new account**: Click "Sign Up"
3. **Login**: Use your credentials
4. **Manage profile**: Visit the profile page
5. **Search flights**: Use the flight search functionality

## API Documentation

### Authentication Backend API Docs
Visit: http://localhost:8001/docs

### Flight Search Backend API Docs
Visit: http://localhost:8000/docs

## Database

The authentication system uses SQLite for simplicity:
- **File**: `backend/auth_database.db`
- **Auto-created**: Tables are created automatically on first run
- **Persistent**: Data persists between restarts

## Security Considerations

### Production Deployment

Before deploying to production:

1. **Change JWT Secret**: Update the secret key in `backend/services/auth_service.py`
2. **Use Environment Variables**: Set proper environment variables
3. **Database Security**: Use a production database (PostgreSQL, MySQL)
4. **HTTPS**: Enable HTTPS for all endpoints
5. **Rate Limiting**: Implement rate limiting for auth endpoints
6. **Email Verification**: Enable email verification
7. **Password Reset**: Implement password reset functionality

### Current Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Session management
- ✅ Input validation
- ✅ CORS protection
- ✅ SQL injection protection (SQLAlchemy)

## Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check if ports 8000 and 8001 are available
   - Ensure all dependencies are installed
   - Check the logs for error messages

2. **Authentication failing**
   - Verify both backends are running
   - Check CORS settings
   - Ensure JWT secret is set

3. **Database issues**
   - Check file permissions for `auth_database.db`
   - Ensure SQLite is available
   - Check database schema

### Logs

- **Authentication Backend**: Check `backend/server.log`
- **Flight Search Backend**: Check console output
- **Frontend**: Check browser console

## Development

### Adding New Features

1. **New API Endpoints**: Add to `backend/api.py`
2. **Database Models**: Add to `backend/models/user.py`
3. **Frontend Components**: Add to `me-tt-a-flights/app/`
4. **API Integration**: Update `me-tt-a-flights/lib/auth-api.ts`

### Testing

```bash
# Test authentication integration
python test_auth_integration.py

# Test individual backends
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## File Structure

```
metta/
├── backend/                    # Authentication Backend
│   ├── api.py                 # FastAPI application
│   ├── models/user.py         # Database models
│   ├── schemas/auth_schemas.py # Pydantic schemas
│   ├── services/auth_service.py # Authentication logic
│   ├── database/database.py   # Database configuration
│   └── auth_database.db       # SQLite database
├── project/                   # Flight Search Backend (unchanged)
│   ├── api.py                # MeTTa flight search API
│   └── Data/flights.metta    # Flight knowledge base
├── me-tt-a-flights/          # Frontend (updated)
│   ├── lib/auth-api.ts       # Authentication API client
│   ├── components/auth-provider.tsx # Auth context
│   ├── app/login/page.tsx    # Login page
│   ├── app/register/page.tsx # Register page
│   └── app/profile/page.tsx  # Profile page
├── start.sh                  # Startup script (updated)
└── test_auth_integration.py  # Integration test
```

## Conclusion

The authentication system is now fully integrated and functional. Users can:

- ✅ Register new accounts
- ✅ Login securely
- ✅ Manage their profiles
- ✅ Access protected features
- ✅ Logout safely

The system maintains the existing MeTTa flight search functionality while adding comprehensive user management capabilities. The separation of concerns ensures that the flight search backend remains unchanged and the authentication system can be developed independently.