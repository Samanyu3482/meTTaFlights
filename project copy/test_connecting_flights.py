#!/usr/bin/env python3
"""
Test script to verify connecting flights functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import load_dataset, smart_search, find_connecting_flights, is_valid_connection, create_connection_flight

def test_connecting_flights():
    """Test the connecting flights functionality"""
    print("=== Testing Connecting Flights Functionality ===")

    # Load the flight data
    try:
        load_dataset("Data_new/flights.metta")
        print("✅ Flight data loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading flight data: {e}")
        return

    # Test parameters
    source = "JFK"
    destination = "LAX"
    year = 2025
    month = 8
    day = 9

    print(f"\nSearching flights: {source} -> {destination} on {year}-{month:02d}-{day:02d}")
    print("=" * 80)

    # Test 1: Direct flights only
    print("\n--- Test 1: Direct Flights Only ---")
    try:
        direct_results = smart_search(
            source=source,
            destination=destination,
            year=year,
            month=month,
            day=day,
            priority="cost",
            include_connections=False
        )
        print(f"Found {len(direct_results)} direct flights")
        
        if direct_results:
            print("Top 3 direct flights:")
            for i, flight in enumerate(direct_results[:3], 1):
                print(f"  {i}. Cost: ${flight['cost']}, Duration: {flight['duration']}min, "
                      f"Takeoff: {flight['takeoff']}, Landing: {flight['landing']}")
        else:
            print("No direct flights found")
    except Exception as e:
        print(f"❌ Error with direct flights: {e}")

    # Test 2: Including connecting flights
    print("\n--- Test 2: Including Connecting Flights ---")
    try:
        all_results = smart_search(
            source=source,
            destination=destination,
            year=year,
            month=month,
            day=day,
            priority="cost",
            include_connections=True
        )
        print(f"Found {len(all_results)} total flights (direct + connecting)")
        
        # Separate direct and connecting flights
        direct_flights = [f for f in all_results if not f.get('is_connecting', False)]
        connecting_flights = [f for f in all_results if f.get('is_connecting', False)]
        
        print(f"  - Direct flights: {len(direct_flights)}")
        print(f"  - Connecting flights: {len(connecting_flights)}")
        
        if connecting_flights:
            print("\nTop 3 connecting flights:")
            for i, flight in enumerate(connecting_flights[:3], 1):
                print(f"  {i}. Cost: ${flight['cost']}, Duration: {flight['duration']}min, "
                      f"Connection: {flight['connection_airport']}, Layover: {flight['layover_hours']}h")
                if flight.get('segments'):
                    for j, segment in enumerate(flight['segments'], 1):
                        print(f"      Segment {j}: {segment['source']}->{segment['destination']} "
                              f"({segment['takeoff']}-{segment['landing']}, {segment['duration']}min)")
        else:
            print("No connecting flights found")
            
    except Exception as e:
        print(f"❌ Error with connecting flights: {e}")

    # Test 3: Different priorities
    print("\n--- Test 3: Different Priorities ---")
    priorities = ["cost", "time", "optimized"]
    
    for priority in priorities:
        print(f"\nPriority: {priority.upper()}")
        try:
            results = smart_search(
                source=source,
                destination=destination,
                year=year,
                month=month,
                day=day,
                priority=priority,
                include_connections=True
            )
            
            if results:
                print(f"Top result: Cost: ${results[0]['cost']}, Duration: {results[0]['duration']}min")
                if results[0].get('is_connecting', False):
                    print(f"  Type: Connecting via {results[0]['connection_airport']}")
                else:
                    print(f"  Type: Direct flight")
            else:
                print("No flights found")
                
        except Exception as e:
            print(f"❌ Error with {priority} priority: {e}")

    # Test 4: Connection validation
    print("\n--- Test 4: Connection Validation ---")
    try:
        # Get some sample flights for testing
        sample_flights = smart_search(year=year, month=month, day=day, include_connections=False)
        
        if len(sample_flights) >= 2:
            flight1 = sample_flights[0]
            flight2 = sample_flights[1]
            
            print(f"Testing connection between:")
            print(f"  Flight 1: {flight1['source']}->{flight1['destination']} ({flight1['takeoff']}-{flight1['landing']})")
            print(f"  Flight 2: {flight2['source']}->{flight2['destination']} ({flight2['takeoff']}-{flight2['landing']})")
            
            is_valid = is_valid_connection(flight1, flight2)
            print(f"  Valid connection: {'✅ Yes' if is_valid else '❌ No'}")
            
            if is_valid:
                connection = create_connection_flight(flight1, flight2)
                if connection:
                    print(f"  Total cost: ${connection['cost']}")
                    print(f"  Total duration: {connection['duration']}min")
                    print(f"  Layover: {connection['layover_hours']}h")
        else:
            print("Not enough sample flights for validation test")
            
    except Exception as e:
        print(f"❌ Error with connection validation: {e}")

    print("\n" + "=" * 80)
    print("✅ Connecting Flights Test Completed!")

def test_specific_route():
    """Test a specific route that might have connecting flights"""
    print("\n=== Testing Specific Route ===")
    
    # Test a route that might not have direct flights but could have connections
    source = "JFK"
    destination = "SFO"  # San Francisco
    year = 2025
    month = 8
    day = 9
    
    print(f"Testing route: {source} -> {destination}")
    
    try:
        # Direct flights
        direct = smart_search(source=source, destination=destination, year=year, month=month, day=day, include_connections=False)
        print(f"Direct flights: {len(direct)}")
        
        # With connections
        all_flights = smart_search(source=source, destination=destination, year=year, month=month, day=day, include_connections=True)
        print(f"Total flights (with connections): {len(all_flights)}")
        
        if all_flights:
            print("\nTop 5 results:")
            for i, flight in enumerate(all_flights[:5], 1):
                flight_type = "Connecting" if flight.get('is_connecting', False) else "Direct"
                print(f"  {i}. [{flight_type}] Cost: ${flight['cost']}, Duration: {flight['duration']}min")
                if flight.get('is_connecting', False):
                    print(f"      Via: {flight['connection_airport']}, Layover: {flight['layover_hours']}h")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Connecting Flights Test")
    print("=" * 50)
    
    test_connecting_flights()
    test_specific_route()
    
    print("\nTest completed!") 