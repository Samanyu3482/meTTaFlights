#!/usr/bin/env python3
"""
Performance test script to compare old vs new search implementation
"""

import time
import sys
import os

def test_old_search():
    """Test the old MeTTa-based search"""
    print("Testing OLD MeTTa-based search...")
    
    try:
        from main import load_dataset, smart_search
        
        # Load data
        start_time = time.time()
        load_dataset("Data_new/flights.metta")
        load_time = time.time() - start_time
        print(f"Data loading time: {load_time:.2f} seconds")
        
        # Test searches
        test_cases = [
            {"source": "JFK", "destination": "ATL", "year": 2025, "month": 8, "day": 9},
            {"source": "LGA", "destination": "ATL", "year": 2025, "month": 8, "day": 10},
            {"source": "JFK", "year": 2025, "month": 8, "day": 8},
            {"destination": "MIA", "year": 2025, "month": 8, "day": 8},
        ]
        
        total_search_time = 0
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest case {i}: {test_case}")
            start_time = time.time()
            results = smart_search(**test_case)
            search_time = time.time() - start_time
            total_search_time += search_time
            print(f"  Results: {len(results)} flights")
            print(f"  Search time: {search_time:.3f} seconds")
        
        print(f"\nTotal search time: {total_search_time:.3f} seconds")
        print(f"Average search time: {total_search_time/len(test_cases):.3f} seconds")
        
    except Exception as e:
        print(f"Error in old search test: {e}")

def test_new_search():
    """Test the new optimized search"""
    print("\n" + "="*50)
    print("Testing NEW optimized search...")
    
    try:
        from optimized_search import initialize_search_engine, smart_search
        
        # Initialize search engine
        start_time = time.time()
        search_engine = initialize_search_engine("Data_new/flights.metta")
        init_time = time.time() - start_time
        print(f"Search engine initialization time: {init_time:.2f} seconds")
        
        # Print stats
        stats = search_engine.get_stats()
        print(f"Search engine stats: {stats}")
        
        # Test searches
        test_cases = [
            {"source": "JFK", "destination": "ATL", "year": 2025, "month": 8, "day": 9},
            {"source": "LGA", "destination": "ATL", "year": 2025, "month": 8, "day": 10},
            {"source": "JFK", "year": 2025, "month": 8, "day": 8},
            {"destination": "MIA", "year": 2025, "month": 8, "day": 8},
        ]
        
        total_search_time = 0
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest case {i}: {test_case}")
            start_time = time.time()
            results = smart_search(**test_case)
            search_time = time.time() - start_time
            total_search_time += search_time
            print(f"  Results: {len(results)} flights")
            print(f"  Search time: {search_time:.3f} seconds")
        
        print(f"\nTotal search time: {total_search_time:.3f} seconds")
        print(f"Average search time: {total_search_time/len(test_cases):.3f} seconds")
        
    except Exception as e:
        print(f"Error in new search test: {e}")

def test_api_endpoints():
    """Test API endpoints performance"""
    print("\n" + "="*50)
    print("Testing API endpoints...")
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        print("\nTesting health endpoint...")
        start_time = time.time()
        response = requests.get(f"{base_url}/health")
        health_time = time.time() - start_time
        print(f"Health check time: {health_time:.3f} seconds")
        print(f"Status: {response.status_code}")
        
        # Test performance stats
        print("\nTesting performance stats...")
        start_time = time.time()
        response = requests.get(f"{base_url}/api/performance/stats")
        stats_time = time.time() - start_time
        print(f"Stats endpoint time: {stats_time:.3f} seconds")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"Stats: {json.dumps(stats, indent=2)}")
        
        # Test flight search
        print("\nTesting flight search endpoint...")
        search_data = {
            "source": "JFK",
            "destination": "ATL",
            "year": 2025,
            "month": 8,
            "day": 9,
            "priority": "cost"
        }
        
        start_time = time.time()
        response = requests.post(f"{base_url}/api/flights/search", json=search_data)
        search_time = time.time() - start_time
        print(f"Flight search time: {search_time:.3f} seconds")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Results: {len(results)} flights")
            print(f"Response headers: {dict(response.headers)}")
        
    except Exception as e:
        print(f"Error in API test: {e}")

if __name__ == "__main__":
    print("Flight Search Performance Test")
    print("="*50)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type == "old":
            test_old_search()
        elif test_type == "new":
            test_new_search()
        elif test_type == "api":
            test_api_endpoints()
        else:
            print("Usage: python test_performance.py [old|new|api]")
    else:
        # Run all tests
        test_old_search()
        test_new_search()
        test_api_endpoints()