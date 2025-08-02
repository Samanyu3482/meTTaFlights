# Unified Booking System

## Overview

The Unified Booking System integrates all three flight search APIs (cheapest, fastest, optimized) with the existing booking system to provide a seamless booking experience. Users can search flights using any of the three APIs and then book directly through a unified interface.

## Architecture

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
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Backend Booking API    │
                    │      (Port 8001)          │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │      Database             │
                    │   (SQLite + Auth DB)      │
                    └───────────────────────────┘
```

## API Endpoints

### Unified Booking API (Port 8004)

#### Health Check
- `GET /api/unified-booking/health`
- Returns health status and integrated API information

#### Booking Operations
- `POST /api/unified-booking/book-flight`
  - Books a flight using details from any search API
  - Requires JWT authentication
  - Accepts flight details, passenger info, and payment info

- `GET /api/unified-booking/user-bookings`
  - Retrieves all bookings for the authenticated user

- `GET /api/unified-booking/booking/{booking_ref}`
  - Gets specific booking details by reference number

- `DELETE /api/unified-booking/booking/{booking_ref}`
  - Cancels a booking

## Data Flow

### 1. Flight Search
1. User searches flights using any of the three APIs
2. Search API returns flight details in unified schema format
3. Frontend displays flight options to user

### 2. Flight Selection
1. User selects a flight from search results
2. Frontend collects passenger and payment information
3. Frontend prepares booking request with flight details

### 3. Booking Process
1. Frontend sends booking request to Unified Booking API
2. Unified Booking API validates JWT token
3. API converts flight details to backend format
4. API forwards booking request to Backend Booking API
5. Backend creates booking in database
6. Booking is automatically added to user's trips

### 4. Confirmation
1. Unified Booking API returns booking confirmation
2. User receives booking reference and e-ticket number
3. Booking appears in user's trips section

## Key Features

### 🔄 **Unified Schema**
- All three search APIs use identical output schemas
- Seamless integration between search and booking
- No data conversion needed for frontend

### 🔐 **Secure Authentication**
- JWT token validation for all booking operations
- User can only access their own bookings
- Secure payment information handling

### 🔗 **Automatic Integration**
- Bookings automatically added to user's trips
- Real-time synchronization with backend system
- Consistent data across all services

### 📊 **Comprehensive Tracking**
- Booking reference numbers for tracking
- E-ticket generation
- Search priority tracking (which API was used)

## Usage Examples

### Frontend Integration

```javascript
// Search flights using any API
const searchResults = await searchFlights({
  source: "JFK",
  destination: "LAX",
  year: 2024,
  month: 3,
  day: 15,
  priority: "cheapest" // or "fastest" or "optimized"
});

// Book selected flight
const bookingResponse = await fetch('/api/unified-booking/book-flight', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${userToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    flight_details: selectedFlight,
    passengers: passengerInfo,
    payment: paymentInfo,
    search_priority: "cheapest"
  })
});
```

### API Response Format

```json
{
  "success": true,
  "message": "Flight booked successfully",
  "booking": {
    "success": true,
    "booking_reference": "BK202403151234567890ABCD",
    "message": "Flight booked successfully! Your booking has been added to your trips.",
    "flight_details": {
      "id": "flight_123",
      "source": "JFK",
      "destination": "LAX",
      "cost": 299.99,
      "airline": {
        "code": "AA",
        "name": "American Airlines"
      }
    },
    "total_amount": 299.99,
    "e_ticket_number": "ET202403151234567890",
    "booking_timestamp": "2024-03-15T12:34:56"
  },
  "search_time_ms": 245.67,
  "search_priority": "cheapest",
  "user_id": "123"
}
```

## Configuration

### Environment Variables

```bash
# API URLs
BACKEND_API_URL=http://localhost:8001
CHEAPEST_API_URL=http://localhost:8001
FASTEST_API_URL=http://localhost:8003
OPTIMIZED_API_URL=http://localhost:8002

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Port Configuration

| Service | Port | Description |
|---------|------|-------------|
| Backend API | 8001 | Main backend with auth and booking |
| Optimized API | 8002 | Optimized flight search |
| Fastest API | 8003 | Fastest flight search |
| Unified Booking API | 8005 | Unified booking interface |

## Testing

Run the integration test:

```bash
cd chatbot-api
python test_unified_booking.py
```

This will test:
- All three search APIs
- Unified booking API health
- Data format compatibility
- Integration readiness

## Benefits

### For Users
- **Seamless Experience**: Search and book in one flow
- **Multiple Options**: Choose from cheapest, fastest, or optimized flights
- **Automatic Organization**: Bookings automatically added to trips
- **Secure**: JWT authentication and secure payment handling

### For Developers
- **Unified Interface**: Single API for all booking operations
- **Consistent Schema**: Same data format across all APIs
- **Easy Integration**: Simple frontend integration
- **Scalable**: Microservices architecture

### For System
- **Data Consistency**: Unified schema prevents data mismatches
- **Error Handling**: Comprehensive error handling and validation
- **Monitoring**: Health checks and performance tracking
- **Security**: JWT validation and secure data handling

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live booking status
2. **Payment Integration**: Stripe/PayPal integration
3. **Email Notifications**: Booking confirmations and updates
4. **Mobile App**: React Native integration
5. **Analytics**: Booking analytics and insights
6. **Multi-currency**: International currency support 