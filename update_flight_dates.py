#!/usr/bin/env python3
"""
Update flight dates in flights.metta to Aug 10-20, 2025 with proper distribution
"""

import re
import random
from collections import defaultdict

def update_flight_dates(input_file, output_file):
    """Update flight dates with proper distribution"""
    
    # Read the original file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Parse all flight entries
    flight_pattern = r'\(flight (\d{4}) (\d{2}) (\d{2}) ([A-Z]{3}) ([A-Z]{3}) (\d+) (\d{4}) (\d{4})\)'
    flights = re.findall(flight_pattern, content)
    
    print(f"Found {len(flights)} flights to update")
    
    # Group flights by route (source-destination)
    route_flights = defaultdict(list)
    for flight in flights:
        year, month, day, source, dest, cost, takeoff, landing = flight
        route = f"{source}-{dest}"
        route_flights[route].append(flight)
    
    print(f"Found {len(route_flights)} unique routes")
    
    # Generate new dates with proper distribution
    new_content = content
    
    # Available dates: Aug 10-20, 2025
    available_dates = [
        (2025, "08", "10"), (2025, "08", "11"), (2025, "08", "12"), 
        (2025, "08", "13"), (2025, "08", "14"), (2025, "08", "15"),
        (2025, "08", "16"), (2025, "08", "17"), (2025, "08", "18"),
        (2025, "08", "19"), (2025, "08", "20")
    ]
    
    # Update each route with distributed dates
    for route, route_flight_list in route_flights.items():
        print(f"Processing route {route} with {len(route_flight_list)} flights")
        
        # Shuffle available dates for this route
        route_dates = available_dates.copy()
        random.shuffle(route_dates)
        
        # Distribute dates among flights for this route
        for i, flight in enumerate(route_flight_list):
            year, month, day, source, dest, cost, takeoff, landing = flight
            
            # Get a date for this flight (cycle through available dates)
            new_year, new_month, new_day = route_dates[i % len(route_dates)]
            
            # Create new flight entry
            old_entry = f"(flight {year} {month} {day} {source} {dest} {cost} {takeoff} {landing})"
            new_entry = f"(flight {new_year} {new_month} {new_day} {source} {dest} {cost} {takeoff} {landing})"
            
            # Replace in content
            new_content = new_content.replace(old_entry, new_entry)
    
    # Write updated content
    with open(output_file, 'w') as f:
        f.write(new_content)
    
    print(f"Updated flights written to {output_file}")
    print("Date distribution summary:")
    
    # Verify distribution
    updated_flights = re.findall(flight_pattern, new_content)
    date_counts = defaultdict(int)
    for flight in updated_flights:
        year, month, day, source, dest, cost, takeoff, landing = flight
        date_counts[f"{year}-{month}-{day}"] += 1
    
    for date in sorted(date_counts.keys()):
        print(f"  {date}: {date_counts[date]} flights")

if __name__ == "__main__":
    input_file = "project copy/Data_new/flights.metta"
    output_file = "project copy/Data_new/flights_updated.metta"
    
    print("🔄 Updating flight dates to Aug 10-20, 2025...")
    update_flight_dates(input_file, output_file)
    print("✅ Date update completed!") 