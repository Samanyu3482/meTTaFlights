# Cheapest Flight Search & Booking API

## 🎯 Overview

This API finds the cheapest flights by integrating with your existing search API and booking system. It asks for flight details in the terminal, searches for flights, finds the cheapest one, and completes the booking process.

## 🚀 How It Works

### **1. Terminal Interface**
- Ask for flight details (source, destination, date, passengers)
- Send request to your existing search API (port 8000)
- Find the cheapest flight from the results
- Complete booking using your existing booking API (port 8001)

### **2. API Endpoints**
- `GET /` - Health check
- `GET /api/cheapest/health` - Detailed health check
- `POST /api/cheapest/search` - Search for cheapest flight
- `POST /api/cheapest/book` - Book the cheapest flight

## 🛠 Quick Start

### **1. Start the API**
```bash
cd chatbot-api/cheapest-api
./start.sh
```

### **2. Use Terminal Interface**
```bash
python main.py --terminal
```

### **3. Test the API**
```bash
python test_cheapest_api.py
```

## 📋 Usage Examples

### **Terminal Interface**
```
🚀 Cheapest Flight Search & Booking System
==================================================

📋 Options:
1. Search for cheapest flight
2. Book a flight
3. Exit

Enter your choice (1-3): 1

🔍 Flight Search
--------------------
From (e.g., New York): New York
To (e.g., London): London
Date (YYYY-MM-DD): 2024-03-15
Number of passengers: 1
Max budget (optional, press Enter to skip): 500

🔍 Searching for cheapest flight...
✅ Found cheapest flight: American Airlines for $350
   Airline: American Airlines
   Flight: AA789
   Price: $350
   Duration: 8h 30m
   Stops: 1
   Departure: 2024-03-15T14:00:00
   Arrival: 2024-03-15T22:30:00
```

### **API Usage**
```bash
# Search for cheapest flight
curl -X POST "http://localhost:8002/api/cheapest/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "New York",
    "destination": "London",
    "date": "2024-03-15",
    "passengers": 1
  }'

# Book a flight
curl -X POST "http://localhost:8002/api/cheapest/book" \
  -H "Content-Type: application/json" \
  -d '{
    "flight_id": "flight_001",
    "passengers": [...],
    "payment": {...}
  }'
```

## 🔧 Integration

### **With Your Existing APIs**
- **Search API**: `http://localhost:8000` (your project copy API)
- **Booking API**: `http://localhost:8001` (your booking API)

### **Response Format**
```json
{
  "success": true,
  "message": "Found cheapest flight: American Airlines for $350",
  "cheapest_flight": {
    "id": "flight_001",
    "airline": "American Airlines",
    "flight_number": "AA789",
    "price": 350.0,
    "duration": "8h 30m",
    "stops": 1
  },
  "total_flights": 5
}
```

## 📊 Features

- ✅ **Terminal Interface**: Easy-to-use command line interface
- ✅ **API Integration**: Works with your existing search and booking APIs
- ✅ **Cheapest Flight Detection**: Automatically finds the lowest price option
- ✅ **Booking Integration**: Completes the full booking process
- ✅ **Error Handling**: Robust error handling and validation
- ✅ **Health Checks**: Monitor API status and integration

## 🧪 Testing

### **Run Tests**
```bash
python test_cheapest_api.py
```

### **Manual Testing**
```bash
# Start terminal interface
python main.py --terminal

# Or test API directly
curl http://localhost:8002/api/cheapest/health
```

## 📖 API Documentation

Once the server is running:
- **Interactive Docs**: `http://localhost:8002/docs`
- **ReDoc**: `http://localhost:8002/redoc`
- **OpenAPI Schema**: `http://localhost:8002/openapi.json`

## 🔄 Workflow

1. **User Input**: Enter flight details in terminal
2. **Search**: API calls your existing search API
3. **Find Cheapest**: Sorts flights by price, picks cheapest
4. **Book**: Completes booking using your existing booking API
5. **Result**: Flight appears in "My Trips" section

## 🚀 Next Steps

- Integrate with your frontend
- Add more search criteria
- Implement fastest and optimized APIs
- Add real-time price tracking

---

**Ready to use!** The API integrates seamlessly with your existing flight booking system. 