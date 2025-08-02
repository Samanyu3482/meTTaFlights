# Unified Booking API

A unified booking API that integrates with the three flight search APIs (cheapest, fastest, optimized) and connects to the existing booking system.

## Features

- **Unified Booking**: Accepts flight details from any of the three search APIs
- **Automatic Integration**: Automatically adds bookings to user's trips section
- **JWT Authentication**: Secure user authentication and authorization
- **Data Conversion**: Converts between different API formats seamlessly
- **Booking Management**: Full CRUD operations for bookings

## API Endpoints

### Health Check
- `GET /api/unified-booking/health` - Check API health and integrated services

### Booking Operations
- `POST /api/unified-booking/book-flight` - Book a flight from search results
- `GET /api/unified-booking/user-bookings` - Get all user bookings
- `GET /api/unified-booking/booking/{booking_ref}` - Get specific booking details
- `DELETE /api/unified-booking/booking/{booking_ref}` - Cancel a booking

## Configuration

Set the following environment variables:

```bash
BACKEND_API_URL=http://localhost:8001
CHEAPEST_API_URL=http://localhost:8001
FASTEST_API_URL=http://localhost:8003
OPTIMIZED_API_URL=http://localhost:8002
SECRET_KEY=your-super-secret-key-change-this-in-production
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
python main.py
```

The API will run on port 8005.

## Usage Example

### Book a Flight

```python
import requests

# Book a flight from search results
booking_request = {
    "flight_details": {
        "id": "flight_123",
        "source": "JFK",
        "destination": "LAX",
        "year": 2024,
        "month": 3,
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
            "logo": "https://example.com/aa-logo.png",
            "description": "American Airlines"
        },
        "flight_number": "AA123",
        "stops": 0,
        "is_connecting": False,
        "connection_airport": None,
        "layover_hours": 0
    },
    "passengers": [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "date_of_birth": "1990-01-01",
            "passport_number": "A12345678",
            "phone": "+1234567890",
            "seat_preference": "window",
            "special_requests": None
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
}

response = requests.post(
    "http://localhost:8005/api/unified-booking/book-flight",
    json=booking_request,
    headers={"Authorization": "Bearer YOUR_JWT_TOKEN"}
)

print(response.json())
```

## Integration Flow

1. **Search APIs** (ports 8001, 8002, 8003) return flight details
2. **Unified Booking API** (port 8004) accepts flight details from any search API
3. **Data Conversion** transforms search API format to backend booking format
4. **Backend API** (port 8001) processes the booking and stores in database
5. **User Trips** automatically updated with new booking

## Error Handling

The API includes comprehensive error handling for:
- Invalid JWT tokens
- Backend service unavailability
- Data conversion errors
- Booking failures
- Network timeouts

## Security

- JWT token validation for all endpoints
- Secure payment information handling
- Input validation and sanitization
- CORS configuration for cross-origin requests 