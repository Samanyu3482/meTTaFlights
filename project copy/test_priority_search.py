#!/usr/bin/env python3
"""
Test script to verify priority-based flight search functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import load_dataset, smart_search, calculate_flight_duration

def test_duration_calculation():
    """Test the duration calculation with fixed data"""
    print("=== Testing Duration Calculation ===")
    
    test_cases = [
        ("0945", "1404", "JFK->LAX morning flight"),
        ("1900", "2334", "JFK->LAX evening flight"),
        ("0500", "0856", "EWR->MSP early morning"),
        ("1645", "1818", "LGA->BGR afternoon"),
    ]
    
    for takeoff, landing, description in test_cases:
        duration = calculate_flight_duration(takeoff, landing)
        print(f"{description}: {takeoff} -> {landing} = {duration} minutes ({duration//60}h {duration%60}m)")
    
    print()

def test_priority_search():
    """Test priority-based search functionality"""
    print("=== Testing Priority-Based Search ===")
    
    # Load the fixed data
    try:
        load_dataset("Data_new/flights.metta")
        print("✅ Flight data loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading flight data: {e}")
        return
    
    # Test search parameters
    source = "JFK"
    destination = "LAX"
    year = 2025
    month = 8
    day = 9
    
    print(f"\nSearching flights: {source} -> {destination} on {year}-{month:02d}-{day:02d}")
    print("=" * 60)
    
    # Test different priorities
    priorities = ["cost", "time", "optimized"]
    
    for priority in priorities:
        print(f"\n--- Priority: {priority.upper()} ---")
        
        try:
            results = smart_search(
                source=source,
                destination=destination,
                year=year,
                month=month,
                day=day,
                priority=priority
            )
            
            print(f"Found {len(results)} flights")
            
            if results:
                print("Top 5 results:")
                for i, flight in enumerate(results[:5], 1):
                    print(f"  {i}. Cost: ${flight['cost']}, Duration: {flight['duration']}min, "
                          f"Takeoff: {flight['takeoff']}, Landing: {flight['landing']}")
            else:
                print("No flights found")
                
        except Exception as e:
            print(f"❌ Error with {priority} priority: {e}")
    
    print("\n" + "=" * 60)

def test_specific_flight():
    """Test a specific flight record to verify data parsing"""
    print("=== Testing Specific Flight Record ===")
    
    try:
        load_dataset("Data_new/flights.metta")
        
        # Search for the specific problematic flight
        results = smart_search(
            source="JFK",
            destination="LAX",
            year=2025,
            month=8,
            day=9
        )
        
        # Find the flight with cost 5085
        target_flight = None
        for flight in results:
            if flight['cost'] == "5085":
                target_flight = flight
                break
        
        if target_flight:
            print(f"Found target flight:")
            print(f"  Cost: ${target_flight['cost']}")
            print(f"  Takeoff: {target_flight['takeoff']}")
            print(f"  Landing: {target_flight['landing']}")
            print(f"  Duration: {target_flight['duration']} minutes")
            
            # Verify duration calculation
            expected_duration = calculate_flight_duration(
                target_flight['takeoff'], 
                target_flight['landing']
            )
            print(f"  Expected duration: {expected_duration} minutes")
            print(f"  Duration match: {'✅' if target_flight['duration'] == expected_duration else '❌'}")
        else:
            print("Target flight not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Priority-Based Flight Search Test")
    print("=" * 50)
    
    test_duration_calculation()
    test_priority_search()
    test_specific_flight()
    
    print("\nTest completed!") 