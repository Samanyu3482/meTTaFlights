#!/usr/bin/env python3
"""
Test script to verify unified API schema across all three flight search APIs
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any

# API endpoints
APIS = {
    "cheapest": "http://localhost:8002/api/cheapest/search",
    "fastest": "http://localhost:8003/api/fastest/search", 
    "optimized": "http://localhost:8004/api/optimized/search"
}

# Test request data
TEST_REQUEST = {
    "source": "JFK",
    "destination": "LAX", 
    "year": 2025,
    "month": 8,
    "day": 4,
    "passengers": 1,
    "cabin_class": "economy",
    "include_connections": True,
    "max_connections": 2
}

# Real JWT token from authentication system
REAL_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU0MDEzNDE3LCJ0eXBlIjoiYWNjZXNzIn0.J6gFEnfXrzPHeR1uoJjHi22MPfcsVGwdNtVgjduppok"

async def test_api(api_name: str, endpoint: str) -> Dict[str, Any]:
    """Test a single API endpoint"""
    print(f"\n{'='*50}")
    print(f"Testing {api_name.upper()} API")
    print(f"{'='*50}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"Making request to: {endpoint}")
            print(f"Request data: {json.dumps(TEST_REQUEST, indent=2)}")
            
            # Add authorization header with REAL JWT token
            headers = {
                "Authorization": f"Bearer {REAL_JWT_TOKEN}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(endpoint, json=TEST_REQUEST, headers=headers)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {api_name} API responded successfully")
                
                # Validate response structure
                validate_response_structure(result, api_name)
                
                return result
            else:
                print(f"❌ {api_name} API failed with status {response.status_code}")
                print(f"Error: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error testing {api_name} API: {str(e)}")
        return None

def validate_response_structure(response: Dict[str, Any], api_name: str):
    """Validate that response follows unified schema"""
    print(f"\nValidating {api_name} API response structure...")
    
    # Required top-level fields
    required_fields = [
        "success", "message", "flight", "total_flights", 
        "search_time_ms", "priority_type", "source", 
        "destination", "search_date"
    ]
    
    for field in required_fields:
        if field not in response:
            print(f"❌ Missing required field: {field}")
            return False
        else:
            print(f"✅ Found field: {field} = {response[field]}")
    
    # Validate priority_type matches API
    expected_priority = api_name
    if response["priority_type"] != expected_priority:
        print(f"❌ Priority type mismatch: expected {expected_priority}, got {response['priority_type']}")
    else:
        print(f"✅ Priority type correct: {response['priority_type']}")
    
    # Validate flight object if present
    if response["success"] and response["flight"]:
        validate_flight_details(response["flight"], api_name)

def validate_flight_details(flight: Dict[str, Any], api_name: str):
    """Validate flight details structure"""
    print(f"\nValidating flight details for {api_name} API...")
    
    # Required flight fields
    required_flight_fields = [
        "id", "source", "destination", "year", "month", "day",
        "departure_time", "arrival_time", "duration", "duration_minutes",
        "cost", "currency", "base_fare", "taxes", "total_fare",
        "airline", "flight_number", "stops", "is_connecting", 
        "layover_hours", "segments", "aircraft", "cabin_class",
        "available_seats", "seat_class", "baggage_allowance",
        "refund_policy", "change_policy", "meal_included",
        "entertainment", "wifi_available", "power_outlets",
        "booking_class", "fare_basis", "ticket_type",
        "search_timestamp", "valid_until"
    ]
    
    for field in required_flight_fields:
        if field not in flight:
            print(f"❌ Missing flight field: {field}")
        else:
            print(f"✅ Found flight field: {field}")
    
    # CRITICAL: Check for passenger_info field
    if "passenger_info" in flight:
        passenger = flight["passenger_info"]
        print(f"✅ Found passenger_info field!")
        print(f"   - Name: {passenger.get('first_name', 'N/A')} {passenger.get('last_name', 'N/A')}")
        print(f"   - Email: {passenger.get('email', 'N/A')}")
        print(f"   - DOB: {passenger.get('date_of_birth', 'N/A')}")
        print(f"   - Passport: {passenger.get('passport_number', 'N/A')}")
        print(f"   - Nationality: {passenger.get('nationality', 'N/A')}")
        print(f"   - Seat Preference: {passenger.get('seat_preference', 'N/A')}")
        print(f"   - Meal Preference: {passenger.get('meal_preference', 'N/A')}")
    else:
        print(f"❌ MISSING passenger_info field - This is required for booking!")
    
    # Validate airline object
    if "airline" in flight:
        airline = flight["airline"]
        required_airline_fields = ["code", "name", "logo", "description"]
        for field in required_airline_fields:
            if field not in airline:
                print(f"❌ Missing airline field: {field}")
            else:
                print(f"✅ Found airline field: {field}")
    
    # Validate baggage_allowance structure
    if "baggage_allowance" in flight:
        baggage = flight["baggage_allowance"]
        if isinstance(baggage, dict) and "checked" in baggage and "carry_on" in baggage:
            print("✅ Baggage allowance structure correct")
        else:
            print("❌ Baggage allowance structure incorrect")

async def test_all_apis():
    """Test all three APIs"""
    print("🚀 Starting unified API schema test")
    print(f"Test time: {datetime.now()}")
    
    results = {}
    
    for api_name, endpoint in APIS.items():
        result = await test_api(api_name, endpoint)
        results[api_name] = result
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    successful_apis = 0
    for api_name, result in results.items():
        if result and result.get("success"):
            successful_apis += 1
            print(f"✅ {api_name.upper()} API: SUCCESS")
            if result.get("flight"):
                flight = result["flight"]
                print(f"   - Airline: {flight.get('airline', {}).get('name', 'Unknown')}")
                print(f"   - Cost: ${flight.get('cost', 0)}")
                print(f"   - Duration: {flight.get('duration', 'Unknown')}")
                print(f"   - Search time: {result.get('search_time_ms', 0):.2f}ms")
        else:
            print(f"❌ {api_name.upper()} API: FAILED")
    
    print(f"\nResults: {successful_apis}/3 APIs working correctly")
    
    if successful_apis == 3:
        print("🎉 All APIs are working with unified schema!")
    else:
        print("⚠️  Some APIs need attention")
    
    return results

async def compare_api_outputs(results: Dict[str, Any]):
    """Compare outputs from different APIs"""
    print(f"\n{'='*60}")
    print("COMPARING API OUTPUTS")
    print(f"{'='*60}")
    
    successful_results = {k: v for k, v in results.items() if v and v.get("success")}
    
    if len(successful_results) < 2:
        print("Need at least 2 successful APIs to compare")
        return
    
    # Compare flight details
    flights = {}
    for api_name, result in successful_results.items():
        if result.get("flight"):
            flights[api_name] = result["flight"]
    
    if len(flights) >= 2:
        print("Comparing flight details across APIs:")
        
        # Compare basic fields
        basic_fields = ["source", "destination", "year", "month", "day"]
        for field in basic_fields:
            values = [flight.get(field) for flight in flights.values()]
            if len(set(values)) == 1:
                print(f"✅ {field}: Consistent across all APIs ({values[0]})")
            else:
                print(f"⚠️  {field}: Inconsistent values {values}")
        
        # Compare costs
        costs = [flight.get("cost", 0) for flight in flights.values()]
        print(f"💰 Cost comparison: {costs}")
        
        # Compare durations
        durations = [flight.get("duration_minutes", 0) for flight in flights.values()]
        print(f"⏱️  Duration comparison (minutes): {durations}")
        
        # Show which API found what
        for api_name, flight in flights.items():
            print(f"\n{api_name.upper()} API found:")
            print(f"  - Airline: {flight.get('airline', {}).get('name', 'Unknown')}")
            print(f"  - Cost: ${flight.get('cost', 0)}")
            print(f"  - Duration: {flight.get('duration', 'Unknown')} ({flight.get('duration_minutes', 0)} minutes)")

if __name__ == "__main__":
    print("🧪 Unified API Schema Test")
    print("This script tests all three flight search APIs to ensure they")
    print("return consistent output using the unified schema.")
    print("\nMake sure all APIs are running:")
    print("- Cheapest API: http://localhost:8002")
    print("- Fastest API: http://localhost:8003") 
    print("- Optimized API: http://localhost:8004")
    
    # Run tests
    results = asyncio.run(test_all_apis())
    
    # Compare outputs
    asyncio.run(compare_api_outputs(results))
    
    print(f"\n✅ Test completed at {datetime.now()}") 