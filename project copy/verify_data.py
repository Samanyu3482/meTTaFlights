#!/usr/bin/env python3
"""
Verify the modified flight data
"""

from main import load_dataset, smart_search

def verify_data():
    print("Verifying modified flight data...")
    
    # Load the data
    load_dataset("Data_new/flights.metta")
    
    # Check JFK -> LAX
    print("\nChecking JFK -> LAX:")
    flights = smart_search(source='JFK', destination='LAX', year=2025, month=8, day=9, include_connections=False)
    print(f"Direct flights: {len(flights)}")
    
    if flights:
        print("Direct flights found:")
        for i, flight in enumerate(flights[:3], 1):
            print(f"  {i}. Cost: ${flight['cost']}, Duration: {flight['duration']}min")
    else:
        print("No direct flights found - this is correct!")
    
    # Check with connections
    print("\nChecking JFK -> LAX with connections:")
    all_flights = smart_search(source='JFK', destination='LAX', year=2025, month=8, day=9, include_connections=True)
    print(f"Total flights: {len(all_flights)}")
    
    direct = [f for f in all_flights if not f.get('is_connecting', False)]
    connecting = [f for f in all_flights if f.get('is_connecting', False)]
    
    print(f"Direct: {len(direct)}, Connecting: {len(connecting)}")
    
    if connecting:
        print("\nConnecting flights found:")
        for i, flight in enumerate(connecting[:3], 1):
            print(f"  {i}. Via {flight['connection_airport']}, Layover: {flight['layover_hours']}h, Cost: ${flight['cost']}")
    
    # Check what flights exist from JFK to ATL (should be many)
    print("\nChecking JFK -> ATL (should be many):")
    atl_flights = smart_search(source='JFK', destination='ATL', year=2025, month=8, day=9, include_connections=False)
    print(f"JFK -> ATL flights: {len(atl_flights)}")
    
    # Check what flights exist from ATL to LAX (should be many)
    print("\nChecking ATL -> LAX (should be many):")
    lax_flights = smart_search(source='ATL', destination='LAX', year=2025, month=8, day=9, include_connections=False)
    print(f"ATL -> LAX flights: {len(lax_flights)}")

if __name__ == "__main__":
    verify_data() 