#!/usr/bin/env python3
"""
Shuffle Flight Dates
Redistributes flights to target August 3-10, 2025 with proportional distribution
"""

import random
from collections import defaultdict
from datetime import datetime, timedelta
import json

def shuffle_flight_dates(input_file: str, output_file: str, target_start_date: str = "2025-08-03", target_end_date: str = "2025-08-10"):
    """
    Shuffle flight dates to target date range with proportional distribution
    
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
    
    # Read all flight records
    flight_records = []
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('(flight '):
                    flight_records.append(line)
    except Exception as e:
        print(f"❌ Error reading {input_file}: {e}")
        return False
    
    total_flights = len(flight_records)
    print(f"📊 Found {total_flights:,} flight records")
    
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
    print(f"\n📅 Flight Distribution:")
    for date, count in date_distribution.items():
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime('%A')
        print(f"  {date} ({day_name}): {count} flights")
    
    # Shuffle flight records
    print(f"\n🔄 Shuffling flight records...")
    random.shuffle(flight_records)
    
    # Distribute flights across dates
    shuffled_flights = []
    flight_index = 0
    
    for date, count in date_distribution.items():
        year, month, day = date.split('-')
        
        # Take 'count' number of flights for this date
        for i in range(count):
            if flight_index < len(flight_records):
                # Parse original flight record
                original_flight = flight_records[flight_index]
                parts = original_flight.strip('()').split()
                
                # Create new flight record with target date
                new_flight = f"(flight {year} {month} {day} {parts[4]} {parts[5]} {parts[6]})"
                shuffled_flights.append(new_flight)
                flight_index += 1
    
    # Verify we used all flights
    if flight_index != total_flights:
        print(f"⚠️ Warning: Used {flight_index} flights out of {total_flights}")
    
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
        return True
    except Exception as e:
        print(f"❌ Error writing shuffled file: {e}")
        return False

def verify_shuffle(input_file: str, target_start_date: str = "2025-08-03", target_end_date: str = "2025-08-10"):
    """Verify the shuffle was successful"""
    print(f"🔍 Verifying shuffle...")
    
    # Parse target dates
    start_date = datetime.strptime(target_start_date, "%Y-%m-%d")
    end_date = datetime.strptime(target_end_date, "%Y-%m-%d")
    
    # Count flights by date
    date_counts = defaultdict(int)
    total_flights = 0
    
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
                        date_key = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                        
                        # Check if date is in target range
                        flight_date = datetime.strptime(date_key, "%Y-%m-%d")
                        if start_date <= flight_date <= end_date:
                            date_counts[date_key] += 1
                            total_flights += 1
    
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    
    print(f"✅ Verification complete!")
    print(f"📊 Total flights in target range: {total_flights:,}")
    print(f"📅 Date distribution:")
    
    sorted_dates = sorted(date_counts.items())
    for date, count in sorted_dates:
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime('%A')
        print(f"  {date} ({day_name}): {count} flights")
    
    return True

def main():
    """Main function"""
    input_file = "Data/flights.metta"
    output_file = "Data/flights_august_2025.metta"
    target_start = "2025-08-03"
    target_end = "2025-08-10"
    
    print("🚀 Flight Date Shuffle Tool")
    print("=" * 50)
    print(f"🎯 Target: {target_start} to {target_end}")
    print(f"📁 Input: {input_file}")
    print(f"📁 Output: {output_file}")
    print("=" * 50)
    
    # Perform the shuffle
    success = shuffle_flight_dates(input_file, output_file, target_start, target_end)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Shuffle completed successfully!")
        
        # Verify the shuffle
        verify_shuffle(output_file, target_start, target_end)
        
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