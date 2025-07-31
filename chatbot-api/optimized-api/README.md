# Optimized Flight Search API

This API finds flights with the **best balance of cost and time** (optimized priority).

## Features

- **Optimized search**: Finds flights with the best balance of cost and time
- **Direct and connecting flights**: Supports both direct and multi-stop flights
- **RESTful API**: Easy-to-use HTTP endpoints
- **Terminal interface**: Command-line interface for testing
- **Real-time search**: Uses the flight search engine for live results

## Installation

1. Navigate to the optimized-api directory:
```bash
cd chatbot-api/optimized-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### API Server Mode

Start the API server:
```bash
python main.py
```

The server will start on `http://localhost:8004`

### Terminal Mode

Run the interactive terminal interface:
```bash
python main.py --terminal
```

## API Endpoints

### Health Check
```
GET /api/optimized/health
```

### Search Optimized Flight (POST)
```
POST /api/optimized/search
```

**Request Body:**
```json
{
  "source": "JFK",
  "destination": "LAX",
  "year": 2024,
  "month": 12,
  "day": 25,
  "include_connections": true,
  "max_connections": 2
}
```

### Search Optimized Flight (GET)
```
GET /api/optimized/search?source=JFK&destination=LAX&year=2024&month=12&day=25
```

### Get Airlines
```
GET /api/optimized/airlines
```

### Get Routes
```
GET /api/optimized/routes
```

## Response Format

```json
{
  "success": true,
  "message": "Optimized flight found from JFK to LAX",
  "optimized_flight": {
    "id": "flight_JFK_LAX_2024_12_25",
    "source": "JFK",
    "destination": "LAX",
    "year": "2024",
    "month": "12",
    "day": "25",
    "takeoff": "08:00",
    "landing": "11:30",
    "duration": "5h 30m",
    "duration_minutes": 330,
    "cost": "450.00",
    "airline": "AA",
    "airline_name": "American Airlines",
    "airline_logo": "aa.png",
    "airline_description": "American Airlines",
    "flight_number": "AA123",
    "stops": 0,
    "departure_time": "08:00",
    "arrival_time": "11:30",
    "is_connecting": false,
    "connection_airport": "",
    "layover_hours": 0
  },
  "total_flights": 15,
  "search_time_ms": 245.67
}
```

## Key Differences from Other APIs

1. **Priority**: Always uses "optimized" priority for best cost-time balance
2. **Sorting**: Uses the search API's optimized sorting algorithm
3. **Focus**: Emphasizes balanced value over pure cost or time
4. **Port**: Runs on port 8004 (vs 8002 for cheapest, 8003 for fastest)

## Examples

### Using curl

```bash
# Search for optimized flight
curl -X POST "http://localhost:8004/api/optimized/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "JFK",
    "destination": "LAX",
    "year": 2024,
    "month": 12,
    "day": 25
  }'

# Health check
curl "http://localhost:8004/api/optimized/health"
```

### Using Python

```python
import requests

# Search for optimized flight
response = requests.post("http://localhost:8004/api/optimized/search", json={
    "source": "JFK",
    "destination": "LAX",
    "year": 2024,
    "month": 12,
    "day": 25
})

result = response.json()
if result["success"]:
    flight = result["optimized_flight"]
    print(f"Optimized flight: {flight['airline_name']} - {flight['duration']} - ${flight['cost']}")
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8004/docs
- **ReDoc**: http://localhost:8004/redoc

## Troubleshooting

1. **Port already in use**: Make sure port 8004 is available
2. **Import errors**: Ensure you're in the correct directory and dependencies are installed
3. **No flights found**: Check that the route exists in the flight data
4. **Performance**: Large searches may take longer, check the `search_time_ms` field 