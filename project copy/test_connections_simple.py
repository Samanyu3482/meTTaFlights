#!/usr/bin/env python3
"""
Simple test for connecting flights
"""

from main import load_dataset, smart_search

def test_connections():
    load_dataset("Data_new/flights.metta")
    
    # Test different routes
    test_routes = [
        ("JFK", "SEA"),
        ("JFK", "MSP"), 
        ("EWR", "LAX"),
        ("JFK", "DFW"),
        ("EWR", "SFO")
    ]
    
    for source, destination in test_routes:
        print(f"\n{'='*50}")
        print(f"Testing {source} -> {destination}")
        print(f"{'='*50}")
        
        flights = smart_search(source=source, destination=destination, year=2025, month=8, day=9, include_connections=True)
        print(f"Total flights: {len(flights)}")
        
        direct = [f for f in flights if not f.get('is_connecting', False)]
        connecting = [f for f in flights if f.get('is_connecting', False)]
        
        print(f"Direct: {len(direct)}, Connecting: {len(connecting)}")
        
        if connecting:
            print("\nConnecting flights found:")
            for i, flight in enumerate(connecting[:3], 1):
                print(f"  {i}. Via {flight['connection_airport']}, Layover: {flight['layover_hours']}h, Cost: ${flight['cost']}")
                if flight.get('segments'):
                    for j, segment in enumerate(flight['segments'], 1):
                        print(f"      Segment {j}: {segment['source']}->{segment['destination']} ({segment['takeoff']}-{segment['landing']})")
        else:
            print("No connecting flights found")
            
            # Let's check what flights are available from source
            print(f"\nChecking flights FROM {source}:")
            source_flights = smart_search(source=source, year=2025, month=8, day=9, include_connections=False)
            destinations = set()
            for flight in source_flights[:30]:  # First 30 flights
                destinations.add(flight['destination'])
            print(f"{source} destinations: {sorted(list(destinations))}")
            
            # Let's check what flights are available TO destination
            print(f"\nChecking flights TO {destination}:")
            dest_flights = smart_search(destination=destination, year=2025, month=8, day=9, include_connections=False)
            sources = set()
            for flight in dest_flights[:30]:  # First 30 flights
                sources.add(flight['source'])
            print(f"{destination} sources: {sorted(list(sources))}")
            
            # Find common airports
            common = destinations.intersection(sources)
            print(f"\nCommon airports (potential connections): {sorted(list(common))}")
            
            if common:
                print(f"\nPotential connection airports found: {len(common)}")
                # Test one of the common airports
                test_connection = list(common)[0]
                print(f"Testing connection via {test_connection}...")
                
                # Get flights from source to connection
                outbound = smart_search(source=source, destination=test_connection, year=2025, month=8, day=9, include_connections=False)
                # Get flights from connection to destination
                inbound = smart_search(source=test_connection, destination=destination, year=2025, month=8, day=9, include_connections=False)
                
                print(f"  Flights {source}->{test_connection}: {len(outbound)}")
                print(f"  Flights {test_connection}->{destination}: {len(inbound)}")
                
                if outbound and inbound:
                    print(f"  Sample outbound: {outbound[0]['takeoff']}-{outbound[0]['landing']}")
                    print(f"  Sample inbound: {inbound[0]['takeoff']}-{inbound[0]['landing']}")

if __name__ == "__main__":
    test_connections() 