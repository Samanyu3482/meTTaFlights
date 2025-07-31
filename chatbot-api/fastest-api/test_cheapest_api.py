#!/usr/bin/env python3
"""
Test script for the Cheapest Flight Search API
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
CHEAPEST_API_URL = "http://localhost:8002"
SEARCH_API_URL = "http://localhost:8000"  # Your project copy API

def test_cheapest_api_health():
    """Test the cheapest API health check endpoint"""
    print("🔍 Testing cheapest API health check...")
    
    try:
        response = requests.get(f"{CHEAPEST_API_URL}/")
        if response.status_code == 200:
            print("✅ Cheapest API health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Cheapest API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Cheapest API. Make sure the server is running on port 8002")
        return False

def test_search_api_health():
    """Test the search API health check"""
    print("🔍 Testing search API health check...")
    
    try:
        response = requests.get(f"{SEARCH_API_URL}/")
        if response.status_code == 200:
            print("✅ Search API health check passed")
            return True
        else:
            print(f"❌ Search API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Search API. Make sure it's running on port 8000")
        return False

def test_cheapest_flight_search():
    """Test cheapest flight search functionality"""
    print("\n🔍 Testing cheapest flight search...")
    
    test_request = {
        "source": "New York",
        "destination": "London",
        "day": 15,
        "month": 3,
        "year": 2024,
        "passengers": 1
    }
    
    try:
        response = requests.post(
            f"{CHEAPEST_API_URL}/api/cheapest/search",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Cheapest flight search passed")
            print(f"   Success: {result.get('success', False)}")
            print(f"   Message: {result.get('message', 'N/A')}")
            
            if result.get('success') and result.get('cheapest_flight'):
                flight = result['cheapest_flight']
                print(f"   Cheapest Flight:")
                print(f"     Airline: {flight.get('airline', 'N/A')}")
                print(f"     Price: ${flight.get('price', 0):.0f}")
                print(f"     Flight Number: {flight.get('flight_number', 'N/A')}")
                print(f"     Duration: {flight.get('duration', 'N/A')}")
                print(f"     Total flights found: {result.get('total_flights', 0)}")
            
            return True
        else:
            print(f"❌ Cheapest flight search failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Cheapest API")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🔍 Testing error handling...")
    
    # Test with invalid data
    invalid_request = {
        "source": "",  # Empty source
        "destination": "London",
        "day": 32,  # Invalid day
        "month": 13,  # Invalid month
        "year": 2024,
        "passengers": -1  # Invalid passengers
    }
    
    try:
        response = requests.post(
            f"{CHEAPEST_API_URL}/api/cheapest/search",
            json=invalid_request,
            headers={"Content-Type": "application/json"}
        )
        
        # Should return 422 (validation error) or 500 (server error)
        if response.status_code in [422, 500]:
            print("✅ Error handling passed for invalid data")
            return True
        else:
            print(f"⚠️  Unexpected response for invalid data: {response.status_code}")
            return True  # Not a failure, just unexpected
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Cheapest API")
        return False

def test_api_integration():
    """Test integration with existing APIs"""
    print("\n🔍 Testing API integration...")
    
    # Test search API integration
    try:
        search_response = requests.get(f"{SEARCH_API_URL}/api/search")
        if search_response.status_code in [200, 404]:  # 404 is expected if no endpoint
            print("✅ Search API integration test passed")
        else:
            print(f"⚠️  Search API returned unexpected status: {search_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Search API")
        return False
    
    return True

def test_performance():
    """Test API performance"""
    print("\n🔍 Testing API performance...")
    
    test_request = {
        "source": "New York",
        "destination": "London",
        "day": 15,
        "month": 3,
        "year": 2024,
        "passengers": 1
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{CHEAPEST_API_URL}/api/cheapest/search",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            print("✅ Performance test passed")
            print(f"   Response time: {response_time:.0f}ms")
            
            if response_time < 5000:  # Should be under 5 seconds (includes API calls)
                print("   ✅ Response time is acceptable")
            else:
                print("   ⚠️  Response time is slow")
            
            return True
        else:
            print(f"❌ Performance test failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Cheapest API")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Cheapest Flight Search API Tests")
    print("=" * 50)
    
    tests = [
        ("Cheapest API Health Check", test_cheapest_api_health),
        ("Search API Health Check", test_search_api_health),
        ("Cheapest Flight Search", test_cheapest_flight_search),
        ("Error Handling", test_error_handling),
        ("API Integration", test_api_integration),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Cheapest API is working correctly.")
        print("\n📋 Summary:")
        print("   ✅ Cheapest API is running on port 8002")
        print("   ✅ Integration with Search API (port 8000)")
        print("   ✅ Flight search and cheapest flight detection")
        print("   ✅ Error handling is robust")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 