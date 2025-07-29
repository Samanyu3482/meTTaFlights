#!/usr/bin/env python3
"""
Detailed Flight Analysis
Analyzes flights.metta to show flight distribution by date and route
"""

from collections import defaultdict, Counter
from datetime import datetime
import json

def analyze_flights_detailed(file_path: str):
    """
    Analyze flights by date and route with detailed breakdown
    """
    print("🔍 Detailed Flight Analysis")
    print("=" * 80)
    
    # Data structures
    date_route_flights = defaultdict(lambda: defaultdict(list))
    date_total_flights = defaultdict(int)
    route_total_flights = defaultdict(int)
    date_route_counts = defaultdict(lambda: defaultdict(int))
    
    # Read and parse flights
    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line.startswith('(flight '):
                    parts = line.strip('()').split()
                    if len(parts) >= 7:
                        year = parts[1]
                        month = parts[2]
                        day = parts[3]
                        source = parts[4]
                        destination = parts[5]
                        cost = parts[6]
                        
                        # Create date and route keys
                        date_key = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                        route = f"{source}-{destination}"
                        
                        # Store flight data
                        flight_data = {
                            'source': source,
                            'destination': destination,
                            'cost': cost,
                            'line_number': line_num
                        }
                        
                        date_route_flights[date_key][route].append(flight_data)
                        date_total_flights[date_key] += 1
                        route_total_flights[route] += 1
                        date_route_counts[date_key][route] += 1
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return
    
    # Summary statistics
    total_flights = sum(date_total_flights.values())
    total_routes = len(route_total_flights)
    total_dates = len(date_total_flights)
    
    print(f"📊 Overall Statistics:")
    print(f"   Total Flights: {total_flights:,}")
    print(f"   Total Routes: {total_routes:,}")
    print(f"   Total Dates: {total_dates}")
    print(f"   Average Flights per Day: {total_flights/total_dates:.1f}")
    print(f"   Average Flights per Route: {total_flights/total_routes:.1f}")
    
    # Date-wise analysis
    print(f"\n📅 Date-wise Flight Distribution:")
    print("-" * 80)
    
    sorted_dates = sorted(date_total_flights.keys())
    for date in sorted_dates:
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime('%A')
        total_on_date = date_total_flights[date]
        routes_on_date = len(date_route_counts[date])
        
        print(f"\n📅 {date} ({day_name})")
        print(f"   Total Flights: {total_on_date:,}")
        print(f"   Unique Routes: {routes_on_date}")
        
        # Show top routes for this date
        top_routes = sorted(date_route_counts[date].items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"   Top Routes:")
        for route, count in top_routes:
            print(f"     {route}: {count} flights")
        
        if routes_on_date > 10:
            print(f"     ... and {routes_on_date - 10} more routes")
    
    # Route-wise analysis
    print(f"\n🛫 Route-wise Flight Distribution:")
    print("-" * 80)
    
    # Show routes with most flights
    top_routes = sorted(route_total_flights.items(), key=lambda x: x[1], reverse=True)[:20]
    print(f"\n🏆 Top 20 Routes by Total Flights:")
    for i, (route, total) in enumerate(top_routes, 1):
        print(f"   {i:2d}. {route}: {total:,} flights")
    
    # Show routes with least flights
    bottom_routes = sorted(route_total_flights.items(), key=lambda x: x[1])[:10]
    print(f"\n📉 Bottom 10 Routes by Total Flights:")
    for i, (route, total) in enumerate(bottom_routes, 1):
        print(f"   {i:2d}. {route}: {total:,} flights")
    
    # Detailed route analysis for sample routes
    print(f"\n🔍 Detailed Analysis for Sample Routes:")
    print("-" * 80)
    
    sample_routes = ["JFK-LAX", "EWR-ATL", "LGA-ORD", "JFK-BOS", "LAX-ORD"]
    
    for route in sample_routes:
        if route in route_total_flights:
            print(f"\n🛫 {route}:")
            print(f"   Total Flights: {route_total_flights[route]:,}")
            
            # Show date distribution for this route
            route_dates = []
            for date in sorted_dates:
                if route in date_route_counts[date]:
                    count = date_route_counts[date][route]
                    route_dates.append((date, count))
            
            print(f"   Date Distribution:")
            for date, count in route_dates:
                day_name = datetime.strptime(date, "%Y-%m-%d").strftime('%A')
                print(f"     {date} ({day_name}): {count} flights")
        else:
            print(f"\n🛫 {route}: Not found in data")
    
    # Route coverage analysis
    print(f"\n📊 Route Coverage Analysis:")
    print("-" * 80)
    
    routes_by_date_count = defaultdict(int)
    for route in route_total_flights:
        date_count = 0
        for date in sorted_dates:
            if route in date_route_counts[date]:
                date_count += 1
        routes_by_date_count[date_count] += 1
    
    print(f"Routes by number of dates they appear on:")
    for date_count in sorted(routes_by_date_count.keys(), reverse=True):
        route_count = routes_by_date_count[date_count]
        percentage = (route_count / total_routes) * 100
        print(f"   {date_count} dates: {route_count} routes ({percentage:.1f}%)")
    
    # Save detailed data to JSON for further analysis
    detailed_data = {
        'summary': {
            'total_flights': total_flights,
            'total_routes': total_routes,
            'total_dates': total_dates,
            'average_flights_per_day': total_flights/total_dates,
            'average_flights_per_route': total_flights/total_routes
        },
        'date_analysis': {
            date: {
                'total_flights': count,
                'unique_routes': len(date_route_counts[date]),
                'routes': dict(date_route_counts[date])
            } for date, count in date_total_flights.items()
        },
        'route_analysis': {
            route: {
                'total_flights': count,
                'date_distribution': {
                    date: date_route_counts[date].get(route, 0)
                    for date in sorted_dates
                }
            } for route, count in route_total_flights.items()
        }
    }
    
    output_file = "flight_analysis_detailed.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(detailed_data, f, indent=2)
        print(f"\n💾 Detailed analysis saved to: {output_file}")
    except Exception as e:
        print(f"⚠️ Could not save detailed analysis: {e}")

def main():
    """Main function"""
    input_file = "Data/flights.metta"
    
    print("🚀 Detailed Flight Analysis Tool")
    print("=" * 80)
    print(f"📁 Analyzing: {input_file}")
    print("=" * 80)
    
    analyze_flights_detailed(input_file)

if __name__ == "__main__":
    main() 