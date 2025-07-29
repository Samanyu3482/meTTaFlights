#!/usr/bin/env python3
"""
Comprehensive Guide: How to Use the Priority-Based Flight Search API

This script demonstrates all ways to interact with the API:
1. Using curl commands
2. Using Python requests
3. Using JavaScript/fetch
4. Direct API calls
"""

import requests
import json
from typing import Dict, Any

# API Base URL
API_BASE = "http://localhost:8000"

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"✅ API Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API not accessible: {e}")
        return False

def search_flights_post_example():
    """Example 1: POST /api/flights/search - Most Flexible Method"""
    print("\n" + "="*60)
    print("EXAMPLE 1: POST /api/flights/search")
    print("="*60)
    
    # Example 1: Search by route and date with cost priority
    payload = {
        "source": "JFK",
        "destination": "LAX", 
        "year": 2025,
        "month": 8,
        "day": 9,
        "priority": "cost"  # "cost", "time", or "optimized"
    }
    
    print(f"Request Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(f"{API_BASE}/api/flights/search", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            flights = response.json()
            print(f"Found {len(flights)} flights")
            print("Top 3 results:")
            for i, flight in enumerate(flights[:3], 1):
                print(f"  {i}. Cost: ${flight['cost']}, Duration: {flight['duration']}min, "
                      f"Takeoff: {flight['takeoff']}, Landing: {flight['landing']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def search_flights_get_examples():
    """Example 2: GET endpoints - Simple searches"""
    print("\n" + "="*60)
    print("EXAMPLE 2: GET /api/flights/route/{source}/{destination}")
    print("="*60)
    
    # Example 2a: Search by route with time priority
    url = f"{API_BASE}/api/flights/route/JFK/LAX?priority=time"
    print(f"Request URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            flights = response.json()
            print(f"Found {len(flights)} flights (sorted by time)")
            print("Top 3 shortest flights:")
            for i, flight in enumerate(flights[:3], 1):
                print(f"  {i}. Duration: {flight['duration']}min, Cost: ${flight['cost']}, "
                      f"Takeoff: {flight['takeoff']}, Landing: {flight['landing']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def search_all_flights_example():
    """Example 3: Get all flights with priority sorting"""
    print("\n" + "="*60)
    print("EXAMPLE 3: GET /api/flights/all")
    print("="*60)
    
    # Example 3: Get all flights with optimized priority
    url = f"{API_BASE}/api/flights/all?priority=optimized"
    print(f"Request URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            flights = response.json()
            print(f"Found {len(flights)} total flights (optimized sorting)")
            print("Top 5 optimized results:")
            for i, flight in enumerate(flights[:5], 1):
                print(f"  {i}. Cost: ${flight['cost']}, Duration: {flight['duration']}min, "
                      f"Route: {flight['source']}→{flight['destination']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def curl_examples():
    """Example 4: curl commands for command line usage"""
    print("\n" + "="*60)
    print("EXAMPLE 4: curl COMMANDS")
    print("="*60)
    
    print("1. Search flights by route with cost priority:")
    print(f'curl -X POST "{API_BASE}/api/flights/search" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{')
    print('       "source": "JFK",')
    print('       "destination": "LAX",')
    print('       "year": 2025,')
    print('       "month": 8,')
    print('       "day": 9,')
    print('       "priority": "cost"')
    print('     }\'')
    print()
    
    print("2. Search flights by route with time priority:")
    print(f'curl "{API_BASE}/api/flights/route/JFK/LAX?priority=time"')
    print()
    
    print("3. Get all flights with optimized priority:")
    print(f'curl "{API_BASE}/api/flights/all?priority=optimized"')
    print()
    
    print("4. Health check:")
    print(f'curl "{API_BASE}/health"')

def javascript_examples():
    """Example 5: JavaScript/fetch examples"""
    print("\n" + "="*60)
    print("EXAMPLE 5: JAVASCRIPT/FETCH EXAMPLES")
    print("="*60)
    
    print("1. Search flights with POST:")
    print("""
fetch('http://localhost:8000/api/flights/search', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        source: 'JFK',
        destination: 'LAX',
        year: 2025,
        month: 8,
        day: 9,
        priority: 'cost'
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
""")
    
    print("2. Search flights with GET:")
    print("""
fetch('http://localhost:8000/api/flights/route/JFK/LAX?priority=time')
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
""")

def priority_explanation():
    """Explain the different priority options"""
    print("\n" + "="*60)
    print("PRIORITY OPTIONS EXPLANATION")
    print("="*60)
    
    print("1. 'cost' - Sort by price (lowest first)")
    print("   - Returns flights sorted by cost in ascending order")
    print("   - Best for budget-conscious travelers")
    print()
    
    print("2. 'time' - Sort by duration (shortest first)")
    print("   - Returns flights sorted by flight duration in ascending order")
    print("   - Best for travelers who want the fastest flights")
    print()
    
    print("3. 'optimized' - Combined optimization")
    print("   - Normalizes both cost and duration to 0-1 range")
    print("   - Calculates combined score: (normalized_cost + normalized_duration) / 2")
    print("   - Returns flights sorted by combined score (lowest first)")
    print("   - Best for travelers who want a balance of cost and time")
    print()

def api_endpoints_summary():
    """Summary of all available endpoints"""
    print("\n" + "="*60)
    print("AVAILABLE API ENDPOINTS")
    print("="*60)
    
    endpoints = [
        {
            "method": "GET",
            "endpoint": "/health",
            "description": "Health check",
            "params": "None"
        },
        {
            "method": "POST", 
            "endpoint": "/api/flights/search",
            "description": "Search flights with full criteria",
            "params": "JSON body with source, destination, year, month, day, priority"
        },
        {
            "method": "GET",
            "endpoint": "/api/flights/route/{source}/{destination}",
            "description": "Search flights by route",
            "params": "priority (query param)"
        },
        {
            "method": "GET",
            "endpoint": "/api/flights/all",
            "description": "Get all flights",
            "params": "priority (query param)"
        }
    ]
    
    for endpoint in endpoints:
        print(f"{endpoint['method']} {endpoint['endpoint']}")
        print(f"  Description: {endpoint['description']}")
        print(f"  Parameters: {endpoint['params']}")
        print()

def main():
    """Run all examples"""
    print("🚀 PRIORITY-BASED FLIGHT SEARCH API USAGE GUIDE")
    print("="*60)
    
    # Test API health first
    if not test_api_health():
        print("❌ Please start the API server first:")
        print("   cd 'project copy'")
        print("   source ../venv/bin/activate")
        print("   python api.py")
        return
    
    # Run all examples
    search_flights_post_example()
    search_flights_get_examples()
    search_all_flights_example()
    curl_examples()
    javascript_examples()
    priority_explanation()
    api_endpoints_summary()
    
    print("✅ API Usage Guide Complete!")
    print("\nTo start the API server:")
    print("   cd 'project copy'")
    print("   source ../venv/bin/activate") 
    print("   python api.py")

if __name__ == "__main__":
    main() 