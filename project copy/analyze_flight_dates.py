#!/usr/bin/env python3
"""
Analyze Flight Dates
Analyzes the dates in flights.metta and counts flights for each date
"""

import re
from collections import defaultdict, Counter
from datetime import datetime
import json

def analyze_flight_dates(file_path: str):
    """Analyze flight dates and count flights per date"""
    
    print("🔄 Analyzing flight dates in flights.metta...")
    
    # Counters for analysis
    date_counts = defaultdict(int)
    month_counts = defaultdict(int)
    year_counts = defaultdict(int)
    total_flights = 0
    
    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line.startswith('(flight '):
                    # Parse flight record: (flight year month day source destination cost)
                    parts = line.strip('()').split()
                    if len(parts) >= 7:
                        year = parts[1]
                        month = parts[2]
                        day = parts[3]
                        
                        # Create date key
                        date_key = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                        month_key = f"{year}-{month.zfill(2)}"
                        
                        # Count flights
                        date_counts[date_key] += 1
                        month_counts[month_key] += 1
                        year_counts[year] += 1
                        total_flights += 1
                        
                        if line_num % 10000 == 0:
                            print(f"📊 Processed {line_num} lines...")
    
    except Exception as e:
        print(f"❌ Error reading flights.metta: {e}")
        return
    
    print(f"✅ Analysis complete! Found {total_flights} total flights")
    
    # Sort dates for better display
    sorted_dates = sorted(date_counts.items())
    sorted_months = sorted(month_counts.items())
    sorted_years = sorted(year_counts.items())
    
    # Display year summary
    print(f"\n📅 Year Summary:")
    for year, count in sorted_years:
        print(f"  {year}: {count:,} flights")
    
    # Display month summary
    print(f"\n📅 Month Summary:")
    for month, count in sorted_months:
        year, month_num = month.split('-')
        month_name = datetime(int(year), int(month_num), 1).strftime('%B')
        print(f"  {month_name} {year}: {count:,} flights")
    
    # Display date details (first 20 and last 20 dates)
    print(f"\n📅 Date Details (showing first 20 and last 20 dates):")
    
    # First 20 dates
    print(f"\n  First 20 dates:")
    for date, count in sorted_dates[:20]:
        year, month, day = date.split('-')
        date_obj = datetime(int(year), int(month), int(day))
        day_name = date_obj.strftime('%A')
        print(f"    {date} ({day_name}): {count} flights")
    
    # Last 20 dates
    print(f"\n  Last 20 dates:")
    for date, count in sorted_dates[-20:]:
        year, month, day = date.split('-')
        date_obj = datetime(int(year), int(month), int(day))
        day_name = date_obj.strftime('%A')
        print(f"    {date} ({day_name}): {count} flights")
    
    # Find busiest and quietest dates
    busiest_date = max(date_counts.items(), key=lambda x: x[1])
    quietest_date = min(date_counts.items(), key=lambda x: x[1])
    
    print(f"\n🏆 Busiest Date:")
    year, month, day = busiest_date[0].split('-')
    date_obj = datetime(int(year), int(month), int(day))
    day_name = date_obj.strftime('%A')
    print(f"  {busiest_date[0]} ({day_name}): {busiest_date[1]} flights")
    
    print(f"\n😴 Quietest Date:")
    year, month, day = quietest_date[0].split('-')
    date_obj = datetime(int(year), int(month), int(day))
    day_name = date_obj.strftime('%A')
    print(f"  {quietest_date[0]} ({day_name}): {quietest_date[1]} flights")
    
    # Calculate average flights per date
    avg_flights_per_date = total_flights / len(date_counts)
    print(f"\n📊 Statistics:")
    print(f"  Total flights: {total_flights:,}")
    print(f"  Unique dates: {len(date_counts):,}")
    print(f"  Average flights per date: {avg_flights_per_date:.1f}")
    print(f"  Date range: {sorted_dates[0][0]} to {sorted_dates[-1][0]}")
    
    # Save detailed results to JSON
    results = {
        "total_flights": total_flights,
        "unique_dates": len(date_counts),
        "date_range": {
            "start": sorted_dates[0][0],
            "end": sorted_dates[-1][0]
        },
        "year_summary": dict(sorted_years),
        "month_summary": dict(sorted_months),
        "date_details": dict(sorted_dates),
        "busiest_date": {
            "date": busiest_date[0],
            "flights": busiest_date[1]
        },
        "quietest_date": {
            "date": quietest_date[0],
            "flights": quietest_date[1]
        },
        "average_flights_per_date": round(avg_flights_per_date, 1)
    }
    
    with open("flight_date_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: flight_date_analysis.json")

def main():
    """Main function"""
    file_path = "Data/flights.metta"
    
    print("🚀 Flight Date Analysis Tool")
    print("=" * 50)
    
    analyze_flight_dates(file_path)

if __name__ == "__main__":
    main() 