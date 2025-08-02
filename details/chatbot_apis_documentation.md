# Chatbot APIs Documentation

## Overview

This document provides detailed information about all 4 APIs in the chatbot-api folder, including their input schemas, output formats, endpoints, and usage examples.

## API Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cheapest API  │    │   Fastest API   │    │ Optimized API   │
│   (Port 8001)   │    │   (Port 8003)   │    │   (Port 8002)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Unified Booking API     │
                    │      (Port 8005)          │
                    └───────────────────────────┘
```

---

## 1. Cheapest API (Port 8001)

### Description
Finds flights with minimum cost (lowest price) from the available flight data.

### Base URL
```
http://localhost:8001
```

### Endpoints

#### Health Check
- **URL**: `/api/cheapest/health`
- **Method**: `GET`
- **Description**: Check API health status

#### Search Flights
- **URL**: `/api/cheapest/search`
- **Method**: `POST`
- **Authentication**: Required (JWT Bearer Token)

### Input Schema

```json
{
  "source": "string",           // Source airport code (e.g., "JFK")
  "destination": "string",      // Destination airport code (e.g., "LAX")
  "year": "integer",           // Year of travel (e.g., 2025)
  "month": "integer",          // Month of travel (1-12)
  "day": "integer",            // Day of travel (1-31)
  "passengers": "integer",     // Number of passengers (default: 1)
  "cabin_class": "string",     // Cabin class preference (default: "economy")
  "include_connections": "boolean", // Include connecting flights (default: true)
  "max_connections": "integer" // Maximum number of connections (default: 2)
}
```

### Output Schema

```json
{
  "success": "boolean",         // Whether search was successful
  "message": "string",         // Response message
  "flight": {
    "id": "string",            // Unique flight identifier
    "source": "string",        // Source airport code
    "destination": "string",   // Destination airport code
    "year": "integer",         // Year of travel
    "month": "integer",        // Month of travel
    "day": "integer",          // Day of travel
    "departure_time": "string", // Departure time (HH:MM)
    "arrival_time": "string",   // Arrival time (HH:MM)
    "duration": "string",       // Total duration (e.g., "3h 30m")
    "duration_minutes": "integer", // Duration in minutes
    "cost": "float",           // Flight cost in USD
    "currency": "string",      // Currency code (default: "USD")
    "base_fare": "float",      // Base fare
    "taxes": "float",          // Taxes and fees
    "total_fare": "float",     // Total fare including taxes
    "airline": {
      "code": "string",        // Airline code (e.g., "AA")
      "name": "string",        // Airline name
      "logo": "string",        // Airline logo URL
      "description": "string"  // Airline description
    },
    "flight_number": "string", // Flight number
    "stops": "integer",        // Number of stops
    "is_connecting": "boolean", // Is this a connecting flight
    "connection_airport": "string", // Connection airport code
    "layover_hours": "float",  // Layover duration in hours
    "segments": "array",       // Individual flight segments
    "aircraft": "string",      // Aircraft type
    "cabin_class": "string",   // Cabin class
    "available_seats": "integer", // Number of available seats
    "seat_class": "string",    // Seat class
    "baggage_allowance": "object", // Baggage allowance details
    "refund_policy": "string", // Refund policy
    "change_policy": "string", // Change policy
    "meal_included": "boolean", // Meal included
    "entertainment": "boolean", // Entertainment available
    "wifi_available": "boolean", // WiFi available
    "power_outlets": "boolean", // Power outlets available
    "booking_class": "string", // Booking class code
    "fare_basis": "string",    // Fare basis code
    "ticket_type": "string",   // Ticket type
    "search_timestamp": "datetime", // When this flight was searched
    "valid_until": "datetime", // When this fare expires
    "passenger_info": "object" // Current user passenger information
  },
  "total_flights": "integer",  // Total flights found
  "search_time_ms": "float",   // Search time in milliseconds
  "priority_type": "string",   // Search priority type ("cheapest")
  "source": "string",          // Source airport
  "destination": "string",     // Destination airport
  "search_date": "string",     // Search date (YYYY-MM-DD)
  "alternative_flights": "array", // Alternative flight options
  "price_history": "object",   // Price history data
  "recommendations": "array"   // Travel recommendations
}
```

---

## 2. Fastest API (Port 8003)

### Description
Finds flights with minimum travel time (shortest duration) from the available flight data.

### Base URL
```
http://localhost:8003
```

### Endpoints

#### Health Check
- **URL**: `/api/fastest/health`
- **Method**: `GET`
- **Description**: Check API health status

#### Search Flights
- **URL**: `/api/fastest/search`
- **Method**: `POST`
- **Authentication**: Required (JWT Bearer Token)

### Input Schema
*Same as Cheapest API*

### Output Schema
*Same as Cheapest API, but with `priority_type: "fastest"`*

---

## 3. Optimized API (Port 8002)

### Description
Finds flights with balanced optimization considering both cost and time factors.

### Base URL
```
http://localhost:8002
```

### Endpoints

#### Health Check
- **URL**: `/api/optimized/health`
- **Method**: `GET`
- **Description**: Check API health status

#### Search Flights
- **URL**: `/api/optimized/search`
- **Method**: `POST`
- **Authentication**: Required (JWT Bearer Token)

### Input Schema
*Same as Cheapest API*

### Output Schema
*Same as Cheapest API, but with `priority_type: "optimized"`*

---

## 4. Unified Booking API (Port 8005)

### Description
Unified booking API that integrates with all three search APIs and connects to the existing booking system.

### Base URL
```
http://localhost:8005
```

### Endpoints

#### Health Check
- **URL**: `/api/unified-booking/health`
- **Method**: `GET`
- **Description**: Check API health status and integrated services

#### Book Flight
- **URL**: `/api/unified-booking/book-flight`
- **Method**: `POST`
- **Authentication**: Required (JWT Bearer Token)

#### Get User Bookings
- **URL**: `/api/unified-booking/user-bookings`
- **Method**: `GET`
- **Authentication**: Required (JWT Bearer Token)

#### Get Booking Details
- **URL**: `/api/unified-booking/booking/{booking_ref}`
- **Method**: `GET`
- **Authentication**: Required (JWT Bearer Token)

#### Cancel Booking
- **URL**: `/api/unified-booking/booking/{booking_ref}`
- **Method**: `DELETE`
- **Authentication**: Required (JWT Bearer Token)

### Input Schema (Book Flight)

```json
{
  "flight_details": {
    "id": "string",            // Unique flight identifier
    "source": "string",        // Source airport code
    "destination": "string",   // Destination airport code
    "year": "integer",         // Year of travel
    "month": "integer",        // Month of travel
    "day": "integer",          // Day of travel
    "departure_time": "string", // Departure time
    "arrival_time": "string",   // Arrival time
    "duration": "string",       // Total duration
    "duration_minutes": "integer", // Duration in minutes
    "cost": "float",           // Flight cost in USD
    "currency": "string",      // Currency code
    "airline": {
      "code": "string",        // Airline code
      "name": "string",        // Airline name
      "logo": "string",        // Airline logo URL
      "description": "string"  // Airline description
    },
    "flight_number": "string", // Flight number
    "stops": "integer",        // Number of stops
    "is_connecting": "boolean", // Is this a connecting flight
    "connection_airport": "string", // Connection airport code
    "layover_hours": "float"   // Layover duration in hours
  },
  "passengers": [
    {
      "first_name": "string",  // First name
      "last_name": "string",   // Last name
      "email": "string",       // Email address
      "date_of_birth": "string", // Date of birth (YYYY-MM-DD)
      "passport_number": "string", // Passport number
      "phone": "string",       // Phone number
      "seat_preference": "string", // Seat preference
      "special_requests": "string" // Special requests
    }
  ],
  "payment": {
    "card_number": "string",   // Card number
    "card_holder_name": "string", // Cardholder name
    "expiry_month": "string",  // Expiry month (MM)
    "expiry_year": "string",   // Expiry year (YYYY)
    "cvv": "string",           // CVV code
    "billing_address": "string", // Billing address
    "city": "string",          // City
    "state": "string",         // State
    "zip_code": "string",      // ZIP code
    "country": "string"        // Country
  },
  "search_priority": "string", // Which search API was used ("cheapest"/"fastest"/"optimized")
  "search_api_response": "object" // Original search API response
}
```

### Output Schema (Book Flight)

```json
{
  "success": "boolean",         // Whether booking was successful
  "message": "string",         // Booking message
  "booking": {
    "success": "boolean",       // Whether booking was successful
    "booking_reference": "string", // Booking reference number
    "message": "string",       // Booking message
    "flight_details": "object", // Confirmed flight details
    "total_amount": "float",   // Total booking amount
    "currency": "string",      // Currency
    "booking_timestamp": "datetime", // Booking timestamp
    "e_ticket_number": "string", // E-ticket number
    "terms_and_conditions": "string" // Terms and conditions
  },
  "search_time_ms": "float",   // Search time in milliseconds
  "search_priority": "string", // Search priority type
  "user_id": "string"          // User ID
}
```

---

## Common Features Across All APIs

### Authentication
All APIs require JWT Bearer Token authentication:
```
Authorization: Bearer <your-jwt-token>
```

### Error Responses
```json
{
  "detail": "Error message description"
}
```

### CORS Support
All APIs support CORS for cross-origin requests.

### Health Check Response
```json
{
  "status": "healthy",
  "service": "API Name",
  "timestamp": "2025-08-02T11:44:34.373892",
  "integrated_apis": {
    "backend_api": "http://localhost:8001",
    "cheapest_api": "http://localhost:8001",
    "fastest_api": "http://localhost:8003",
    "optimized_api": "http://localhost:8002"
  }
}
```

---

## Usage Examples

### 1. Search for Cheapest Flight
```bash
curl -X POST "http://localhost:8001/api/cheapest/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "source": "JFK",
    "destination": "LAX",
    "year": 2025,
    "month": 8,
    "day": 15,
    "include_connections": true,
    "max_connections": 2
  }'
```

### 2. Search for Fastest Flight
```bash
curl -X POST "http://localhost:8003/api/fastest/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "source": "JFK",
    "destination": "LAX",
    "year": 2025,
    "month": 8,
    "day": 15,
    "include_connections": true,
    "max_connections": 2
  }'
```

### 3. Book a Flight
```bash
curl -X POST "http://localhost:8005/api/unified-booking/book-flight" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "flight_details": {
      "id": "flight_JFK_LAX_2025_08_15",
      "source": "JFK",
      "destination": "LAX",
      "year": 2025,
      "month": 8,
      "day": 15,
      "departure_time": "10:00",
      "arrival_time": "13:30",
      "duration": "3h 30m",
      "duration_minutes": 210,
      "cost": 299.99,
      "currency": "USD",
      "airline": {
        "code": "AA",
        "name": "American Airlines",
        "logo": "/airline-logos/aa.png",
        "description": "American Airlines"
      },
      "flight_number": "AA123",
      "stops": 0,
      "is_connecting": false,
      "connection_airport": null,
      "layover_hours": 0
    },
    "passengers": [
      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "date_of_birth": "1990-01-01",
        "passport_number": "A12345678",
        "phone": "+1234567890",
        "seat_preference": "window",
        "special_requests": null
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
    "search_priority": "cheapest"
  }'
```

### 4. Get User Bookings
```bash
curl -X GET "http://localhost:8005/api/unified-booking/user-bookings" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Integration Flow

1. **User Authentication**: Get JWT token from backend auth API
2. **Flight Search**: Use any of the three search APIs (cheapest/fastest/optimized)
3. **Flight Selection**: User selects a flight from search results
4. **Booking**: Use unified booking API to book the selected flight
5. **Confirmation**: Booking is automatically added to user's trips

---

## Notes

- All APIs use the same output schema for consistency
- The unified booking API automatically converts between different data formats
- All bookings are automatically associated with the authenticated user
- The system supports multiple users with proper data isolation
- All APIs include comprehensive error handling and validation 