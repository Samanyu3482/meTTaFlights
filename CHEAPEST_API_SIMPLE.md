# 🚀 Cheapest Flight API - Simple Version

## 🎯 **What It Does**

1. **Takes Input**: source, destination, day, month, year, passengers
2. **Calls Project Copy API**: Sends request to your existing search API (port 8000)
3. **Finds Cheapest**: Sorts flights by price and returns the cheapest one
4. **Returns Result**: Flight details with price, airline, duration, etc.

## 🚀 **How to Run**

### **1. Start the API**
```bash
cd chatbot-api/cheapest-api
python main.py
```

### **2. Use Terminal Interface**
```bash
python main.py --terminal
```

### **3. Test the API**
```bash
python test_cheapest_api.py
```

## 🎯 **Example Usage**

### **Terminal Interface**
```
🚀 Cheapest Flight Search System
========================================

📋 Options:
1. Search for cheapest flight
2. Exit

Enter your choice (1-2): 1

🔍 Flight Search
--------------------
From (e.g., New York): New York
To (e.g., London): London
Day (1-31): 15
Month (1-12): 3
Year (e.g., 2024): 2024
Number of passengers: 1

🔍 Searching for flights from New York to London on 15/3/2024...
📋 Finding the cheapest flight...

✅ Found cheapest flight: American Airlines for $350
   Airline: American Airlines
   Flight: AA789
   Price: $350
   Duration: 8h 30m
   Stops: 1
   Departure: 2024-03-15T14:00:00
   Arrival: 2024-03-15T22:30:00
   Total flights found: 5
```

### **API Endpoint**
```bash
curl -X POST "http://localhost:8002/api/cheapest/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "New York",
    "destination": "London",
    "day": 15,
    "month": 3,
    "year": 2024,
    "passengers": 1
  }'
```

## 📊 **Response Format**
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
  "total_flights": 5,
  "search_date": "2024-03-15",
  "source": "New York",
  "destination": "London"
}
```

## 🔧 **Integration**

- **Search API**: `http://localhost:8000` (your project copy API)
- **Cheapest API**: `http://localhost:8002` (this API)

## 📋 **Features**

- ✅ **Simple Input**: Just source, destination, day, month, year
- ✅ **API Integration**: Works with your existing search API
- ✅ **Cheapest Detection**: Automatically finds the lowest price
- ✅ **No Booking**: Just search and return results
- ✅ **Terminal Interface**: Easy-to-use command line interface

## 🎉 **Ready to Use!**

Your cheapest flight API is now simplified and ready to use! 🚀 