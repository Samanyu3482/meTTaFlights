# 🚀 Cheapest Flight API - Complete Implementation

## 🎯 **What We Built**

A **Cheapest Flight Search & Booking API** that:
1. **Asks for flight details in terminal**
2. **Sends request to your existing search API** (project copy folder)
3. **Finds the cheapest flight** from the results
4. **Completes the booking process** using your existing booking API
5. **Shows the booked flight in "My Trips"** section

## 📁 **Project Structure**

```
chatbot-api/
└── cheapest-api/
    ├── main.py               # Main API (Port 8002)
    ├── test_cheapest_api.py  # Test script
    ├── requirements.txt       # Dependencies
    ├── start.sh              # Startup script
    └── README.md             # Documentation
```

## 🚀 **How to Run**

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

## 🎯 **How It Works**

### **Step 1: Terminal Interface**
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
```

### **Step 2: API Integration**
- **Search API**: Calls your existing search API on port 8000
- **Find Cheapest**: Sorts flights by price, picks the cheapest
- **Booking API**: Uses your existing booking API on port 8001

### **Step 3: Results**
```
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

### **Step 4: Booking**
```
🎫 Flight Booking
--------------------
Flight ID: flight_001
Number of passengers: 1

Passenger 1:
First Name: John
Last Name: Doe
Date of Birth (YYYY-MM-DD): 1990-01-01
Passport Number: 123456789
Email: john@example.com
Phone: 1234567890
Seat Preference (window/aisle): window
Special Requests (optional): 

Payment Details:
Card Number: 1234567890123456
Card Holder Name: John Doe
Expiry Month (MM): 12
Expiry Year (YYYY): 2025
CVV: 123
Billing Address: 123 Main St
City: New York
State: NY
ZIP Code: 10001
Country: United States

🎫 Processing booking...
✅ Flight booked successfully!
🎉 Your flight has been booked! Check 'My Trips' section.
```

## 📊 **API Endpoints**

### **Health Check**
```bash
curl http://localhost:8002/api/cheapest/health
```

### **Search for Cheapest Flight**
```bash
curl -X POST "http://localhost:8002/api/cheapest/search" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "New York",
    "destination": "London",
    "date": "2024-03-15",
    "passengers": 1
  }'
```

### **Book a Flight**
```bash
curl -X POST "http://localhost:8002/api/cheapest/book" \
  -H "Content-Type: application/json" \
  -d '{
    "flight_id": "flight_001",
    "passengers": [...],
    "payment": {...}
  }'
```

## 🔧 **Integration with Your System**

### **APIs Connected**
- **Search API**: `http://localhost:8000` (your project copy API)
- **Booking API**: `http://localhost:8001` (your booking API)

### **Data Flow**
```
Terminal Input → Cheapest API → Search API → Find Cheapest → Booking API → My Trips
```

## 📋 **Features**

- ✅ **Terminal Interface**: Easy-to-use command line interface
- ✅ **API Integration**: Works with your existing search and booking APIs
- ✅ **Cheapest Flight Detection**: Automatically finds the lowest price option
- ✅ **Booking Integration**: Completes the full booking process
- ✅ **Error Handling**: Robust error handling and validation
- ✅ **Health Checks**: Monitor API status and integration

## 🧪 **Testing**

### **Run Full Test Suite**
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

## 📖 **Documentation**

Once running:
- **Interactive Docs**: `http://localhost:8002/docs`
- **ReDoc**: `http://localhost:8002/redoc`
- **OpenAPI Schema**: `http://localhost:8002/openapi.json`

## 🎉 **Ready to Use!**

### **Quick Start**
1. **Start**: `./start.sh`
2. **Use**: `python main.py --terminal`
3. **Test**: `python test_cheapest_api.py`

### **What Happens**
1. **User enters flight details** in terminal
2. **API searches** using your existing search API
3. **Finds cheapest flight** from results
4. **Completes booking** using your existing booking API
5. **Flight appears** in "My Trips" section

**Your cheapest flight API is now complete and ready to integrate with your existing system!** 🚀 