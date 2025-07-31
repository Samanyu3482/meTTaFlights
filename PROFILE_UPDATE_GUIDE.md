# Profile Update & Booking Persistence Guide

## Overview
This guide covers both the profile update functionality and booking persistence system. Both features have been implemented to store data in the backend database, ensuring that user information and bookings persist across sessions.

## 🔧 **What Was Implemented**

### Backend (Already Working)
- ✅ **User Model**: Extended with profile fields (phone, date_of_birth, nationality, address, emergency_contact)
- ✅ **Profile Update API**: `PUT /api/auth/profile` endpoint
- ✅ **Database Schema**: SQLite database with all necessary fields
- ✅ **Authentication**: JWT-based authentication with proper token handling

### Backend (New - Booking System)
- ✅ **Booking Models**: Complete booking, passenger, and payment models
- ✅ **Booking API**: Full CRUD operations for bookings (`POST /api/bookings`, `GET /api/bookings`, etc.)
- ✅ **Booking Service**: Comprehensive booking management service
- ✅ **Database Relationships**: Proper relationships between users, bookings, passengers, and payments

### Frontend (Updated)
- ✅ **Auth Provider**: Updated to use real backend API instead of mock data
- ✅ **Profile Update Function**: `updateProfile()` function that calls the backend
- ✅ **Token Management**: Proper JWT token storage and usage
- ✅ **Error Handling**: Comprehensive error handling for API calls
- ✅ **Booking API Service**: New service to handle booking operations with backend
- ✅ **Trips Page**: Updated to use backend API instead of localStorage
- ✅ **Booking Page**: Updated to create bookings in backend database

## 🚀 **How It Works**

### 1. **User Registration/Login**
```typescript
// When user logs in, the auth provider:
// 1. Calls the backend login API
// 2. Stores JWT tokens in localStorage
// 3. Fetches and stores user data
```

### 2. **Profile Update Process**
```typescript
// When user saves profile:
// 1. Frontend calls updateProfile() with new data
// 2. Auth provider sends PUT request to /api/auth/profile
// 3. Backend validates and updates database
// 4. Updated user data is returned and stored
```

### 3. **Data Persistence**
```typescript
// On subsequent logins:
// 1. Auth provider checks for stored JWT token
// 2. Calls /api/auth/me to get current user data
// 3. Profile data is loaded from database
// 4. User sees their previously saved information
```

### 4. **Booking Persistence**
```typescript
// When user books a flight:
// 1. Frontend sends booking data to /api/bookings
// 2. Backend creates booking record in database
// 3. Booking is associated with user account
// 4. On login, bookings are loaded from database
// 5. User sees all their bookings in "My Trips"
```

## 🧪 **Testing the Functionality**

### Prerequisites
1. **Start Both Backend Servers**:
   
   **Option A: Use the convenience script (Recommended)**:
   ```bash
   ./start_servers.sh
   ```
   
   **Option B: Start manually**:
   ```bash
   # Terminal 1 - Flight Search API (port 8000)
   cd "project copy"
   python api.py
   
   # Terminal 2 - Authentication API (port 8001)
   cd backend
   python api.py
   ```
   
   The servers will start on:
   - Flight Search API: `http://localhost:8000`
   - Authentication API: `http://localhost:8001`

2. **Start the Frontend**:
   ```bash
   cd me-tt-a-flights
   npm run dev
   ```
   The frontend should start on `http://localhost:3000`

### Test Steps

#### Option 1: Manual Testing
1. **Register a new account** at `http://localhost:3000/register`
2. **Log in** with your credentials
3. **Go to Profile page** (`http://localhost:3000/profile`)
4. **Edit your profile** information:
   - Full Name
   - Phone Number
   - Date of Birth
   - Nationality
   - Address
   - Emergency Contact
5. **Click "Save Changes"**
6. **Log out and log back in**
7. **Verify** that your profile data is still there

#### Option 2: Automated Testing
Run the test scripts:
```bash
# Test profile updates
python test_profile_update.py

# Test booking functionality
python test_booking_integration.py
```

These scripts will:
- Register test users
- Test profile updates and persistence
- Test booking creation and persistence
- Verify data remains after logout/login

## 📊 **Database Schema**

The database includes these tables:

**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    date_of_birth VARCHAR(10),
    nationality VARCHAR(100),
    address TEXT,
    emergency_contact TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Bookings Table:**
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    booking_ref VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed',
    flight_year VARCHAR(4) NOT NULL,
    flight_month VARCHAR(2) NOT NULL,
    flight_day VARCHAR(2) NOT NULL,
    source VARCHAR(10) NOT NULL,
    destination VARCHAR(10) NOT NULL,
    cost VARCHAR(20) NOT NULL,
    takeoff VARCHAR(4) NOT NULL,
    landing VARCHAR(4) NOT NULL,
    duration INTEGER NOT NULL,
    airline_code VARCHAR(10),
    airline_name VARCHAR(100),
    airline_logo VARCHAR(255),
    airline_description TEXT,
    is_connecting BOOLEAN DEFAULT FALSE,
    connection_airport VARCHAR(10),
    layover_hours FLOAT,
    total_cost FLOAT NOT NULL,
    passenger_count INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Passengers Table:**
```sql
CREATE TABLE passengers (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth VARCHAR(10) NOT NULL,
    passport_number VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    seat_preference VARCHAR(20) DEFAULT 'window',
    special_requests TEXT,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);
```

**Payments Table:**
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    card_holder_name VARCHAR(100) NOT NULL,
    expiry_month VARCHAR(2) NOT NULL,
    expiry_year VARCHAR(4) NOT NULL,
    billing_address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);
```

## 🔐 **Security Features**

- **JWT Authentication**: All profile updates require valid JWT tokens
- **Input Validation**: Backend validates all input data
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **Password Hashing**: Passwords are hashed with bcrypt
- **Token Expiration**: Access tokens expire after 30 minutes

## 🛠 **API Endpoints**

### Profile Update
```
PUT /api/auth/profile
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "Updated Name",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01",
  "nationality": "US",
  "address": "123 Street, City, State",
  "emergency_contact": "Emergency Contact Info"
}
```

### Get Current User
```
GET /api/auth/me
Authorization: Bearer <jwt_token>
```

### Booking Endpoints

#### Create Booking
```
POST /api/bookings
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "flight": {
    "year": "2024",
    "month": "12",
    "day": "25",
    "source": "JFK",
    "destination": "LAX",
    "cost": "299",
    "takeoff": "0830",
    "landing": "1145",
    "duration": 375,
    "airline": {
      "code": "DL",
      "name": "Delta Airlines",
      "logo": "/airline-logos/dl.png",
      "description": "Delta Airlines"
    }
  },
  "passengers": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-01",
      "passport_number": "US123456789",
      "email": "john@example.com",
      "phone": "+1234567890",
      "seat_preference": "window"
    }
  ],
  "payment": {
    "card_number": "4111111111111111",
    "card_holder_name": "John Doe",
    "expiry_month": "12",
    "expiry_year": "2025",
    "cvv": "123",
    "billing_address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "United States"
  },
  "passenger_count": 1
}
```

#### Get User Bookings
```
GET /api/bookings
Authorization: Bearer <jwt_token>
```

#### Get Upcoming Bookings
```
GET /api/bookings/upcoming
Authorization: Bearer <jwt_token>
```

#### Get Completed Bookings
```
GET /api/bookings/completed
Authorization: Bearer <jwt_token>
```

#### Update Booking Status
```
PUT /api/bookings/{booking_id}/status
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "status": "cancelled"
}
```

#### Delete Booking
```
DELETE /api/bookings/{booking_id}
Authorization: Bearer <jwt_token>
```

## 🐛 **Troubleshooting**

### Common Issues

1. **"No authentication token found"**
   - Make sure you're logged in
   - Check if JWT token is stored in localStorage

2. **"Profile update failed"**
   - Check if backend server is running
   - Verify API endpoint is accessible
   - Check browser console for detailed errors

3. **"Could not connect to backend"**
   - Ensure both backend servers are running:
     - Flight Search API on port 8000
     - Authentication API on port 8001
   - Check if CORS is properly configured
   - Use `./start_servers.sh` to start both servers

4. **Profile data not persisting**
   - Check database file exists: `backend/auth_database.db`
   - Verify database schema is correct
   - Check backend logs for errors

### Debug Steps
1. **Check Backend Logs**: Look for errors in the terminal running `python api.py`
2. **Check Browser Console**: Look for network errors or JavaScript errors
3. **Check Database**: Use SQLite browser to inspect the users table
4. **Test API Directly**: Use tools like Postman or curl to test endpoints

## 📝 **Code Structure**

### Key Files Modified
- `me-tt-a-flights/components/auth-provider.tsx` - Updated to use real API
- `backend/api.py` - Profile update endpoint (already existed)
- `backend/models/user.py` - User model with profile fields (already existed)
- `backend/services/auth_service.py` - Profile update logic (already existed)

### Key Functions
- `updateProfile()` - Frontend function to update profile
- `update_user_profile()` - Backend service function
- `PUT /api/auth/profile` - API endpoint for profile updates

## 🎯 **Success Criteria**

The profile update functionality is working correctly when:
- ✅ Users can save profile information
- ✅ Data persists in the database
- ✅ Data is available after logout/login
- ✅ All profile fields are properly stored and retrieved
- ✅ Error handling works for invalid data
- ✅ Authentication is required for profile updates

## 🚀 **Next Steps**

Potential enhancements:
- Profile picture upload
- Email verification
- Password change functionality
- Two-factor authentication
- Profile data export/import
- Account deletion 