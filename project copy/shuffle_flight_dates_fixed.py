#!/usr/bin/env python3
"""
Shuffle Flight Dates - Fixed Version
Redistributes flights to target August 3-10, 2025 ensuring same routes are on different dates
"""

import random
from collections import defaultdict
from datetime import datetime, timedelta
import json

def shuffle_flight_dates_fixed(input_file: str, output_file: str, target_start_date: str = "2025-08-03", target_end_date: str = "2025-08-10"):
    """
    Shuffle flight dates ensuring same routes are distributed across different dates
    
    Args:
        input_file: Path to input flights.metta file
        output_file: Path to output shuffled flights.metta file
        target_start_date: Start date in YYYY-MM-DD format
        target_end_date: End date in YYYY-MM-DD format
    """
    
    print(f"🔄 Shuffling flight dates to {target_start_date} to {target_end_date}...")
    
    # Parse target dates
    start_date = datetime.strptime(target_start_date, "%Y-%m-%d")
    end_date = datetime.strptime(target_end_date, "%Y-%m-%d")
    
    # Calculate date range
    date_range = (end_date - start_date).days + 1
    print(f"📅 Target date range: {date_range} days")
    
    # Read all flight records and group by route
    route_flights = defaultdict(list)
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('(flight '):
                    parts = line.strip('()').split()
                    if len(parts) >= 7:
                        source = parts[4]
                        destination = parts[5]
                        route = f"{source}-{destination}"
                        route_flights[route].append(line)
    except Exception as e:
        print(f"❌ Error reading {input_file}: {e}")
        return False
    
    total_flights = sum(len(flights) for flights in route_flights.values())
    total_routes = len(route_flights)
    print(f"📊 Found {total_flights:,} flights across {total_routes:,} unique routes")
    
    # Calculate flights per day (proportional distribution)
    flights_per_day = total_flights // date_range
    remainder = total_flights % date_range
    
    print(f"📈 Flights per day: {flights_per_day} (base) + {remainder} (distributed)")
    
    # Create date distribution
    date_distribution = {}
    current_date = start_date
    
    for i in range(date_range):
        day_flights = flights_per_day
        if i < remainder:  # Distribute remainder flights across first few days
            day_flights += 1
        
        date_key = current_date.strftime("%Y-%m-%d")
        date_distribution[date_key] = day_flights
        current_date += timedelta(days=1)
    
    # Display distribution
    print(f"\n📅 Target Flight Distribution:")
    for date, count in date_distribution.items():
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime('%A')
        print(f"  {date} ({day_name}): {count} flights")
    
    # Distribute flights ensuring same routes are on different dates
    print(f"\n🔄 Distributing flights by route...")
    
    # Create target dates list
    target_dates = []
    current_date = start_date
    for i in range(date_range):
        target_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    # Distribute flights for each route across different dates
    shuffled_flights = []
    date_flight_counts = defaultdict(int)
    
    for route, flights in route_flights.items():
        # Shuffle the flights for this route
        random.shuffle(flights)
        
        # Distribute flights across different dates
        for i, flight in enumerate(flights):
            # Choose a date for this flight (cycle through dates)
            date_index = i % len(target_dates)
            target_date = target_dates[date_index]
            
            # Parse original flight record
            parts = flight.strip('()').split()
            year, month, day = target_date.split('-')
            
            # Create new flight record with target date
            new_flight = f"(flight {year} {month} {day} {parts[4]} {parts[5]} {parts[6]})"
            shuffled_flights.append(new_flight)
            date_flight_counts[target_date] += 1
    
    # Shuffle the final list to randomize the order
    random.shuffle(shuffled_flights)
    
    # Create backup
    backup_file = f"{input_file}.backup"
    try:
        with open(backup_file, 'w') as f:
            with open(input_file, 'r') as original:
                f.write(original.read())
        print(f"💾 Created backup: {backup_file}")
    except Exception as e:
        print(f"⚠️ Warning: Could not create backup: {e}")
    
    # Write shuffled flights
    try:
        with open(output_file, 'w') as f:
            for flight in shuffled_flights:
                f.write(flight + '\n')
        print(f"✅ Shuffled flights saved: {output_file}")
        
        # Display actual distribution
        print(f"\n📅 Actual Flight Distribution:")
        sorted_dates = sorted(date_flight_counts.items())
        for date, count in sorted_dates:
            day_name = datetime.strptime(date, "%Y-%m-%d").strftime('%A')
            print(f"  {date} ({day_name}): {count} flights")
        
        return True
    except Exception as e:
        print(f"❌ Error writing shuffled file: {e}")
        return False

def verify_route_distribution(input_file: str, sample_routes: list = None):
    """Verify that flights for the same route are distributed across different dates"""
    print(f"🔍 Verifying route distribution...")
    
    # Group flights by route and check date distribution
    route_dates = defaultdict(set)
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('(flight '):
                    parts = line.strip('()').split()
                    if len(parts) >= 7:
                        year = parts[1]
                        month = parts[2]
                        day = parts[3]
                        source = parts[4]
                        destination = parts[5]
                        route = f"{source}-{destination}"
                        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                        route_dates[route].add(date)
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    
    # Analyze distribution
    total_routes = len(route_dates)
    routes_with_multiple_dates = 0
    max_dates_per_route = 0
    
    for route, dates in route_dates.items():
        if len(dates) > 1:
            routes_with_multiple_dates += 1
        max_dates_per_route = max(max_dates_per_route, len(dates))
    
    print(f"✅ Route distribution verification complete!")
    print(f"📊 Total routes: {total_routes:,}")
    print(f"📊 Routes with multiple dates: {routes_with_multiple_dates:,}")
    print(f"📊 Routes with single date: {total_routes - routes_with_multiple_dates:,}")
    print(f"📊 Maximum dates per route: {max_dates_per_route}")
    print(f"📊 Percentage with multiple dates: {(routes_with_multiple_dates/total_routes)*100:.1f}%")
    
    # Show sample routes if provided
    if sample_routes:
        print(f"\n🔍 Sample route analysis:")
        for route in sample_routes:
            if route in route_dates:
                dates = sorted(route_dates[route])
                print(f"  {route}: {len(dates)} dates - {', '.join(dates)}")
            else:
                print(f"  {route}: Not found")
    
    return True

def main():
    """Main function"""
    input_file = "Data/flights.metta"
    output_file = "Data/flights_august_2025_fixed.metta"
    target_start = "2025-08-03"
    target_end = "2025-08-10"
    
    print("🚀 Flight Date Shuffle Tool - Fixed Version")
    print("=" * 60)
    print(f"🎯 Target: {target_start} to {target_end}")
    print(f"📁 Input: {input_file}")
    print(f"📁 Output: {output_file}")
    print("=" * 60)
    
    # Perform the shuffle
    success = shuffle_flight_dates_fixed(input_file, output_file, target_start, target_end)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Shuffle completed successfully!")
        
        # Verify the route distribution
        sample_routes = ["JFK-LAX", "EWR-ATL", "LGA-ORD", "JFK-BOS"]
        verify_route_distribution(output_file, sample_routes)
        
        print(f"\n📁 Files:")
        print(f"  Original: {input_file}")
        print(f"  Shuffled: {output_file}")
        print(f"  Backup: {input_file}.backup")
        
        print(f"\n🔄 Next steps:")
        print(f"  1. Review the shuffled file: {output_file}")
        print(f"  2. If satisfied, replace the original:")
        print(f"     mv {output_file} {input_file}")
        print(f"  3. Restart your API server to use the new data")
        
    else:
        print("❌ Shuffle failed!")

if __name__ == "__main__":
    main() 