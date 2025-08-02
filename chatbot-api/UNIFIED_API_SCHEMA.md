# Unified Flight Search API Schema

This document describes the unified schema used across all three flight search APIs (Cheapest, Fastest, and Optimized) to ensure consistent output types and complete booking information.

## Overview

All three APIs now use the same input and output schemas, making them compatible for integration with a common booking system. Each API returns the same `FlightSearchResponse` structure with a `FlightDetails` object containing all necessary information for flight booking.

## API Endpoints

### 1. Cheapest Flight API (Port 8002)
- **POST** `/api/cheapest/search` - Find the cheapest flight
- **GET** `/api/cheapest/health` - Health check

### 2. Fastest Flight API (Port 8003)
- **POST** `/api/fastest/search` - Find the fastest flight
- **GET** `/api/fastest/health` - Health check

### 3. Optimized Flight API (Port 8004)
- **POST** `/api/optimized/search` - Find the best balance of cost and time
- **GET** `/api/optimized/health` - Health check

## Request Schema

### FlightSearchRequest
```json
{
  "source": "JFK",
  "destination": "LAX",
  "year": 2024,
  "month": 12,
  "day": 25,
  "passengers": 1,
  "cabin_class": "economy",
  "include_connections": true,
  "max_connections": 2
}
```

**Fields:**
- `source` (string, required): Source airport code
- `destination` (string, required): Destination airport code
- `year` (integer, required): Year of travel
- `month` (integer, required): Month of travel (1-12)
- `day` (integer, required): Day of travel (1-31)
- `passengers` (integer, optional): Number of passengers (default: 1)
- `cabin_class` (string, optional): Cabin class preference (economy, premium_economy, business, first)
- `include_connections` (boolean, optional): Include connecting flights (default: true)
- `max_connections` (integer, optional): Maximum number of connections (default: 2)

## Response Schema

### FlightSearchResponse
```json
{
  "success": true,
  "message": "Found cheapest flight: American Airlines for $299",
  "flight": {
    "id": "flight_JFK_LAX_2024_12_25",
    "source": "JFK",
    "destination": "LAX",
    "year": 2024,
    "month": 12,
    "day": 25,
    "departure_time": "10:30",
    "arrival_time": "13:45",
    "duration": "5h 15m",
    "duration_minutes": 315,
    "cost": 299.0,
    "currency": "USD",
    "base_fare": 254.15,
    "taxes": 44.85,
    "total_fare": 299.0,
    "airline": {
      "code": "AA",
      "name": "American Airlines",
      "logo": "https://example.com/aa-logo.png",
      "description": "American Airlines"
    },
    "flight_number": "AA123",
    "stops": 0,
    "is_connecting": false,
    "connection_airport": null,
    "layover_hours": 0,
    "segments": [],
    "aircraft": "Boeing 737",
    "cabin_class": "economy",
    "available_seats": 50,
    "seat_class": "Economy",
    "baggage_allowance": {
      "checked": 1,
      "carry_on": 1
    },
    "refund_policy": "Non-refundable",
    "change_policy": "Change fee applies",
    "meal_included": true,
    "entertainment": true,
    "wifi_available": false,
    "power_outlets": true,
    "booking_class": "Y",
    "fare_basis": "YOW",
    "ticket_type": "Electronic",
    "search_timestamp": "2024-01-15T10:30:00Z",
    "valid_until": "2024-01-16T10:30:00Z"
  },
  "total_flights": 15,
  "search_time_ms": 245.67,
  "priority_type": "cheapest",
  "source": "JFK",
  "destination": "LAX",
  "search_date": "2024-12-25",
  "alternative_flights": [],
  "price_history": null,
  "recommendations": null
}
```

## FlightDetails Schema

The `flight` object contains complete information needed for booking:

### Basic Flight Information
- `id`: Unique flight identifier
- `source`: Source airport code
- `destination`: Destination airport code
- `year`, `month`, `day`: Travel date

### Timing Information
- `departure_time`: Departure time (HH:MM)
- `arrival_time`: Arrival time (HH:MM)
- `duration`: Human-readable duration (e.g., "5h 15m")
- `duration_minutes`: Duration in minutes

### Pricing Information
- `cost`: Total flight cost in USD
- `currency`: Currency code (USD)
- `base_fare`: Base fare amount
- `taxes`: Taxes and fees
- `total_fare`: Total fare including taxes

### Airline Information
- `airline`: Airline details object
  - `code`: Airline code (e.g., "AA")
  - `name`: Airline name
  - `logo`: Airline logo URL
  - `description`: Airline description
- `flight_number`: Flight number

### Route Information
- `stops`: Number of stops
- `is_connecting`: Whether this is a connecting flight
- `connection_airport`: Connection airport code (if applicable)
- `layover_hours`: Layover duration in hours
- `segments`: Array of individual flight segments for multi-stop flights

### Aircraft and Cabin Information
- `aircraft`: Aircraft type
- `cabin_class`: Cabin class (economy, premium_economy, business, first)

### Booking Details
- `available_seats`: Number of available seats
- `seat_class`: Seat class description
- `baggage_allowance`: Baggage allowance details
- `refund_policy`: Refund policy
- `change_policy`: Change policy

### Additional Services
- `meal_included`: Whether meal is included
- `entertainment`: Whether entertainment is available
- `wifi_available`: Whether WiFi is available
- `power_outlets`: Whether power outlets are available

### Booking Metadata
- `booking_class`: Booking class code
- `fare_basis`: Fare basis code
- `ticket_type`: Ticket type (Electronic)

### Timestamps
- `search_timestamp`: When this flight was searched
- `valid_until`: When this fare expires

## Booking Schema

For future booking integration, the following schemas are available:

### PassengerInfo
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "passport_number": "A12345678",
  "nationality": "US",
  "seat_preference": "window",
  "meal_preference": "vegetarian"
}
```

### ContactInfo
```json
{
  "email": "john.doe@example.com",
  "phone": "+1-555-123-4567",
  "address": "123 Main St",
  "city": "New York",
  "country": "US",
  "postal_code": "10001"
}
```

### PaymentInfo
```json
{
  "card_type": "Visa",
  "card_number": "****-****-****-1234",
  "expiry_date": "12/25",
  "cvv": "123",
  "cardholder_name": "John Doe",
  "billing_address": "123 Main St, New York, NY 10001"
}
```

### BookingRequest
```json
{
  "flight_id": "flight_JFK_LAX_2024_12_25",
  "passengers": [PassengerInfo],
  "contact_info": ContactInfo,
  "payment_info": PaymentInfo,
  "special_requests": "Wheelchair assistance needed",
  "insurance": false
}
```

### BookingResponse
```json
{
  "success": true,
  "booking_reference": "BK123456789",
  "message": "Booking confirmed successfully",
  "flight_details": FlightDetails,
  "total_amount": 299.0,
  "currency": "USD",
  "booking_timestamp": "2024-01-15T10:30:00Z",
  "e_ticket_number": "ET123456789",
  "terms_and_conditions": "Standard terms apply..."
}
```

## Priority Types

The `priority_type` field indicates which search algorithm was used:

- `"cheapest"`: Found the lowest cost flight
- `"fastest"`: Found the shortest duration flight
- `"optimized"`: Found the best balance of cost and time

## Usage Examples

### Python Example
```python
import httpx
import asyncio

async def search_flights():
    async with httpx.AsyncClient() as client:
        # Search for cheapest flight
        response = await client.post(
            "http://localhost:8002/api/cheapest/search",
            json={
                "source": "JFK",
                "destination": "LAX",
                "year": 2024,
                "month": 12,
                "day": 25,
                "passengers": 1
            }
        )
        
        result = response.json()
        if result["success"]:
            flight = result["flight"]
            print(f"Found {result['priority_type']} flight:")
            print(f"  Airline: {flight['airline']['name']}")
            print(f"  Cost: ${flight['cost']}")
            print(f"  Duration: {flight['duration']}")
            print(f"  Departure: {flight['departure_time']}")
            print(f"  Arrival: {flight['arrival_time']}")

# Run the search
asyncio.run(search_flights())
```

### cURL Example
```bash
# Search for cheapest flight
curl -X POST "http://localhost:8002/api/cheapest/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "JFK",
    "destination": "LAX",
    "year": 2024,
    "month": 12,
    "day": 25,
    "passengers": 1
  }'

# Search for fastest flight
curl -X POST "http://localhost:8003/api/fastest/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "JFK",
    "destination": "LAX",
    "year": 2024,
    "month": 12,
    "day": 25,
    "passengers": 1
  }'

# Search for optimized flight
curl -X POST "http://localhost:8004/api/optimized/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "JFK",
    "destination": "LAX",
    "year": 2024,
    "month": 12,
    "day": 25,
    "passengers": 1
  }'
```

## Integration Benefits

1. **Consistent Output**: All APIs return the same response structure
2. **Complete Booking Info**: All necessary details for booking are included
3. **Future-Ready**: Ready for integration with booking systems
4. **Type Safety**: Strong typing with Pydantic models
5. **Documentation**: Comprehensive API documentation with OpenAPI/Swagger

## Next Steps

1. **Booking API**: Create a unified booking API that accepts `FlightDetails` and `BookingRequest`
2. **Payment Integration**: Integrate with payment processors
3. **Email Confirmations**: Send booking confirmations via email
4. **Mobile App**: Create mobile app using the unified API structure
5. **Analytics**: Track booking patterns and flight preferences

## Error Handling

All APIs return consistent error responses:

```json
{
  "success": false,
  "message": "Error description",
  "flight": null,
  "total_flights": 0,
  "search_time_ms": 123.45,
  "priority_type": "cheapest",
  "source": "JFK",
  "destination": "LAX",
  "search_date": "2024-12-25"
}
```

## Health Checks

Each API provides a health check endpoint:

```bash
curl http://localhost:8002/api/cheapest/health
curl http://localhost:8003/api/fastest/health
curl http://localhost:8004/api/optimized/health
```

This unified schema ensures that all three APIs can be easily integrated into a common booking system while providing all the necessary information for complete flight booking functionality. 