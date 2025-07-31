#!/usr/bin/env python3
"""
Test script for the Fastest Flight Search API
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8003"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/fastest/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_fastest_flight_search():
    """Test the fastest flight search endpoint"""
    print("\nTesting fastest flight search...")
    
    # Test data
    test_request = {
        "source": "JFK",
        "destination": "LAX",
        "year": 2024,
        "month": 12,
        "day": 25,
        "include_connections": True,
        "max_connections": 2
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/fastest/search",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                flight = data["fastest_flight"]
                print(f"✅ Fastest flight found!")
                print(f"   Route: {flight['source']} → {flight['destination']}")
                print(f"   Airline: {flight['airline_name']}")
                print(f"   Duration: {flight['duration']}")
                print(f"   Cost: ${flight['cost']}")
                print(f"   Stops: {flight['stops']}")
                print(f"   Total flights searched: {data['total_flights']}")
                print(f"   Search time: {data['search_time_ms']:.2f}ms")
                return True
            else:
                print(f"❌ Search failed: {data['message']}")
                return False
        else:
            print(f"❌ Search request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_get_airlines():
    """Test the airlines endpoint"""
    print("\nTesting airlines endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/fastest/airlines")
        if response.status_code == 200:
            airlines = response.json()
            print(f"✅ Found {len(airlines)} airlines")
            # Show first few airlines
            for airline in airlines[:3]:
                print(f"   - {airline['code']}: {airline['name']}")
            return True
        else:
            print(f"❌ Airlines request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Airlines error: {e}")
        return False

def test_get_routes():
    """Test the routes endpoint"""
    print("\nTesting routes endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/fastest/routes")
        if response.status_code == 200:
            routes = response.json()
            print(f"✅ Found {len(routes)} routes")
            # Show first few routes
            for route in routes[:3]:
                print(f"   - {route['source']} → {route['destination']} ({route['airline_name']})")
            return True
        else:
            print(f"❌ Routes request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Routes error: {e}")
        return False

def test_multiple_searches():
    """Test multiple flight searches"""
    print("\nTesting multiple flight searches...")
    
    test_routes = [
        {"source": "JFK", "destination": "LAX", "name": "JFK → LAX"},
        {"source": "LAX", "destination": "JFK", "name": "LAX → JFK"},
        {"source": "ORD", "destination": "DFW", "name": "ORD → DFW"},
    ]
    
    successful_searches = 0
    
    for route in test_routes:
        print(f"\nSearching {route['name']}...")
        test_request = {
            "source": route["source"],
            "destination": route["destination"],
            "year": 2024,
            "month": 12,
            "day": 25,
            "include_connections": True,
            "max_connections": 2
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/fastest/search",
                json=test_request,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    flight = data["fastest_flight"]
                    print(f"   ✅ Found: {flight['airline_name']} - {flight['duration']} - ${flight['cost']}")
                    successful_searches += 1
                else:
                    print(f"   ❌ No flights found: {data['message']}")
            else:
                print(f"   ❌ Request failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Successful searches: {successful_searches}/{len(test_routes)}")
    return successful_searches > 0

def main():
    """Run all tests"""
    print("🚀 Fastest Flight API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Fastest Flight Search", test_fastest_flight_search),
        ("Get Airlines", test_get_airlines),
        ("Get Routes", test_get_routes),
        ("Multiple Searches", test_multiple_searches),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Fastest Flight API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API server and try again.")
    
    return passed == total

if __name__ == "__main__":
    main() 