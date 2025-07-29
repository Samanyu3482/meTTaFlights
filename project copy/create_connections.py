#!/usr/bin/env python3
"""
Script to modify airport codes in flights.metta to create connection opportunities
This will ensure about 30% of flights become connecting flights
"""

import random
import re

def create_connection_opportunities():
    """Modify airport codes to create connection opportunities"""
    
    # Define major hub airports that will serve as connection points
    hub_airports = ['ATL', 'ORD', 'DFW', 'DEN', 'LAX', 'CLT', 'LAS', 'MCO', 'MIA', 'PHX']
    
    # Define route modifications to create connections
    # Format: (original_source, original_dest, new_source, new_dest, connection_hub)
    route_modifications = [
        # JFK routes - create connections via major hubs
        ('JFK', 'LAX', 'JFK', 'ATL', 'ATL'),  # JFK -> ATL -> LAX
        ('JFK', 'SFO', 'JFK', 'ORD', 'ORD'),  # JFK -> ORD -> SFO
        ('JFK', 'SEA', 'JFK', 'DEN', 'DEN'),  # JFK -> DEN -> SEA
        ('JFK', 'MSP', 'JFK', 'CLT', 'CLT'),  # JFK -> CLT -> MSP
        
        # EWR routes - create connections via major hubs
        ('EWR', 'LAX', 'EWR', 'DFW', 'DFW'),  # EWR -> DFW -> LAX
        ('EWR', 'SFO', 'EWR', 'LAS', 'LAS'),  # EWR -> LAS -> SFO
        ('EWR', 'SEA', 'EWR', 'DEN', 'DEN'),  # EWR -> DEN -> SEA
        ('EWR', 'MSP', 'EWR', 'ORD', 'ORD'),  # EWR -> ORD -> MSP
        
        # LGA routes - create connections via major hubs
        ('LGA', 'LAX', 'LGA', 'ATL', 'ATL'),  # LGA -> ATL -> LAX
        ('LGA', 'SFO', 'LGA', 'ORD', 'ORD'),  # LGA -> ORD -> SFO
        ('LGA', 'SEA', 'LGA', 'DEN', 'DEN'),  # LGA -> DEN -> SEA
        ('LGA', 'MSP', 'LGA', 'CLT', 'CLT'),  # LGA -> CLT -> MSP
        
        # Create more connections for other major routes
        ('JFK', 'BUR', 'JFK', 'LAS', 'LAS'),  # JFK -> LAS -> BUR
        ('JFK', 'FLL', 'JFK', 'MCO', 'MCO'),  # JFK -> MCO -> FLL
        ('JFK', 'TPA', 'JFK', 'MIA', 'MIA'),  # JFK -> MIA -> TPA
        ('JFK', 'SJU', 'JFK', 'MIA', 'MIA'),  # JFK -> MIA -> SJU
        
        ('EWR', 'BUR', 'EWR', 'PHX', 'PHX'),  # EWR -> PHX -> BUR
        ('EWR', 'FLL', 'EWR', 'MCO', 'MCO'),  # EWR -> MCO -> FLL
        ('EWR', 'TPA', 'EWR', 'MIA', 'MIA'),  # EWR -> MIA -> TPA
        ('EWR', 'SJU', 'EWR', 'MIA', 'MIA'),  # EWR -> MIA -> SJU
        
        ('LGA', 'BUR', 'LGA', 'LAS', 'LAS'),  # LGA -> LAS -> BUR
        ('LGA', 'FLL', 'LGA', 'MCO', 'MCO'),  # LGA -> MCO -> FLL
        ('LGA', 'TPA', 'LGA', 'MIA', 'MIA'),  # LGA -> MIA -> TPA
        ('LGA', 'SJU', 'LGA', 'MIA', 'MIA'),  # LGA -> MIA -> SJU
    ]
    
    # Read the original file
    with open('Data_new/flights.metta', 'r') as f:
        content = f.read()
    
    # Create a backup
    with open('Data_new/flights.metta.backup', 'w') as f:
        f.write(content)
    
    print("✅ Created backup: Data_new/flights.metta.backup")
    
    # Track modifications
    modifications_made = 0
    total_flights = 0
    
    # Process each flight record
    lines = content.split('\n')
    modified_lines = []
    
    for line in lines:
        if line.strip().startswith('(flight '):
            total_flights += 1
            
            # Parse the flight record
            match = re.match(r'\(flight (\d{4}) (\d{2}) (\d{2}) (\w+) (\w+) (\d+) (\d{4}) (\d{4})\)', line.strip())
            if match:
                year, month, day, source, dest, cost, takeoff, landing = match.groups()
                
                # Check if this route should be modified
                route_key = (source, dest)
                modified = False
                
                for orig_src, orig_dest, new_src, new_dest, hub in route_modifications:
                    if route_key == (orig_src, orig_dest):
                        # Modify this flight to create a connection opportunity
                        # We'll change the destination to the hub airport
                        modified_line = f'(flight {year} {month} {day} {new_src} {new_dest} {cost} {takeoff} {landing})'
                        modified_lines.append(modified_line)
                        modifications_made += 1
                        modified = True
                        print(f"Modified: {source}->{dest} -> {new_src}->{new_dest} (via {hub})")
                        break
                
                if not modified:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)
    
    # Write the modified content
    with open('Data_new/flights.metta', 'w') as f:
        f.write('\n'.join(modified_lines))
    
    print(f"\n✅ Modified {modifications_made} out of {total_flights} flights ({modifications_made/total_flights*100:.1f}%)")
    print("✅ This should create connection opportunities for about 30% of flights")
    
    # Now we need to add the connecting flights (second segments)
    print("\n🔄 Adding connecting flight segments...")
    
    # Add connecting flights for each modification
    additional_flights = []
    
    for orig_src, orig_dest, new_src, new_dest, hub in route_modifications:
        # Find flights that now go to the hub
        hub_flights = []
        for line in modified_lines:
            if line.strip().startswith('(flight '):
                match = re.match(r'\(flight (\d{4}) (\d{2}) (\d{2}) (\w+) (\w+) (\d+) (\d{4}) (\d{4})\)', line.strip())
                if match:
                    year, month, day, source, dest, cost, takeoff, landing = match.groups()
                    if source == new_src and dest == new_dest:
                        hub_flights.append((year, month, day, source, dest, cost, takeoff, landing))
        
        # Create connecting flights from hub to original destination
        for year, month, day, source, dest, cost, takeoff, landing in hub_flights:
            # Calculate a reasonable connecting flight time (1-3 hours later)
            takeoff_hour = int(takeoff[:2])
            takeoff_minute = int(takeoff[2:])
            
            # Add 1-3 hours for layover
            layover_hours = random.randint(1, 3)
            new_takeoff_hour = (takeoff_hour + layover_hours) % 24
            new_takeoff = f"{new_takeoff_hour:02d}{takeoff_minute:02d}"
            
            # Calculate landing time (assume 2-4 hour flight)
            flight_hours = random.randint(2, 4)
            new_landing_hour = (new_takeoff_hour + flight_hours) % 24
            new_landing_minute = (takeoff_minute + random.randint(0, 59)) % 60
            new_landing = f"{new_landing_hour:02d}{new_landing_minute:02d}"
            
            # Generate a reasonable cost for the connecting flight
            connecting_cost = random.randint(int(cost) * 3 // 4, int(cost) * 5 // 4)
            
            # Create the connecting flight
            connecting_flight = f'(flight {year} {month} {day} {hub} {orig_dest} {connecting_cost} {new_takeoff} {new_landing})'
            additional_flights.append(connecting_flight)
    
    # Add the connecting flights to the file
    with open('Data_new/flights.metta', 'a') as f:
        f.write('\n')
        for flight in additional_flights:
            f.write(flight + '\n')
    
    print(f"✅ Added {len(additional_flights)} connecting flight segments")
    print(f"✅ Total flights now: {total_flights + len(additional_flights)}")
    print("✅ Connection opportunities created successfully!")

if __name__ == "__main__":
    print("🚀 Creating Connection Opportunities in Flight Dataset")
    print("=" * 60)
    create_connection_opportunities()
    print("\n✅ Process completed!") 