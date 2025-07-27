#!/usr/bin/env python3
"""
Route Analyzer for MeTTa Flight Data
Analyzes flight patterns and maps routes to real airlines
"""

import re
import json
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

def parse_flights_file(file_path: str) -> List[Tuple[str, str, str]]:
    """Parse flights.metta file and extract route information"""
    routes = []
    
    with open(file_path, 'r') as f:
        for line in f:
            # Match pattern: (flight year month day source destination cost)
            match = re.match(r'\(flight (\d{4}) (\d{1,2}) (\d{1,2}) (\w{3}) (\w{3}) (\d+)\)', line.strip())
            if match:
                year, month, day, source, destination, cost = match.groups()
                routes.append((source, destination, cost))
    
    return routes

def analyze_route_patterns(routes: List[Tuple[str, str, str]]) -> Dict:
    """Analyze route patterns and frequency"""
    route_counts = Counter()
    source_airports = set()
    destination_airports = set()
    
    for source, destination, cost in routes:
        route = f"{source}-{destination}"
        route_counts[route] += 1
        source_airports.add(source)
        destination_airports.add(destination)
    
    # Get top routes by frequency
    top_routes = route_counts.most_common(50)
    
    return {
        'total_flights': len(routes),
        'unique_routes': len(route_counts),
        'source_airports': len(source_airports),
        'destination_airports': len(destination_airports),
        'top_routes': top_routes,
        'route_frequencies': dict(route_counts)
    }

def create_airline_mapping() -> Dict:
    """Create mapping of routes to real airlines based on 2013 data"""
    
    # Major US airlines and their typical routes in 2013
    airline_routes = {
        'AA': {  # American Airlines
            'name': 'American Airlines',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/American_Airlines_logo_2013.svg/200px-American_Airlines_logo_2013.svg.png',
            'description': 'Major US airline with extensive domestic network',
            'hub_routes': ['JFK', 'LAX', 'ORD', 'DFW', 'MIA', 'CLT'],
            'typical_routes': [
                'JFK-LAX', 'JFK-SFO', 'JFK-MIA', 'JFK-ORD', 'JFK-DFW',
                'LAX-JFK', 'LAX-ORD', 'LAX-DFW', 'LAX-MIA',
                'ORD-JFK', 'ORD-LAX', 'ORD-MIA', 'ORD-DFW',
                'DFW-JFK', 'DFW-LAX', 'DFW-ORD', 'DFW-MIA',
                'MIA-JFK', 'MIA-LAX', 'MIA-ORD', 'MIA-DFW'
            ]
        },
        'UA': {  # United Airlines
            'name': 'United Airlines',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/United_Airlines_Logo.svg/200px-United_Airlines_Logo.svg.png',
            'description': 'Major US airline with global network',
            'hub_routes': ['EWR', 'ORD', 'DEN', 'SFO', 'LAX', 'IAD'],
            'typical_routes': [
                'EWR-LAX', 'EWR-SFO', 'EWR-ORD', 'EWR-DEN', 'EWR-IAD',
                'ORD-EWR', 'ORD-LAX', 'ORD-SFO', 'ORD-DEN',
                'DEN-EWR', 'DEN-ORD', 'DEN-LAX', 'DEN-SFO',
                'SFO-EWR', 'SFO-ORD', 'SFO-DEN', 'SFO-LAX'
            ]
        },
        'DL': {  # Delta Air Lines
            'name': 'Delta Air Lines',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Delta_logo.svg/200px-Delta_logo.svg.png',
            'description': 'Major US airline with extensive domestic and international network',
            'hub_routes': ['JFK', 'ATL', 'DTW', 'MSP', 'SLC', 'LAX'],
            'typical_routes': [
                'JFK-ATL', 'JFK-DTW', 'JFK-MSP', 'JFK-SLC',
                'ATL-JFK', 'ATL-DTW', 'ATL-MSP', 'ATL-SLC',
                'DTW-JFK', 'DTW-ATL', 'DTW-MSP', 'DTW-SLC',
                'MSP-JFK', 'MSP-ATL', 'MSP-DTW', 'MSP-SLC'
            ]
        },
        'WN': {  # Southwest Airlines
            'name': 'Southwest Airlines',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Southwest_Airlines_logo_2014.svg/200px-Southwest_Airlines_logo_2014.svg.png',
            'description': 'Low-cost carrier with point-to-point service',
            'hub_routes': ['BWI', 'MDW', 'HOU', 'PHX', 'LAS', 'DEN'],
            'typical_routes': [
                'BWI-MDW', 'BWI-HOU', 'BWI-PHX', 'BWI-LAS',
                'MDW-BWI', 'MDW-HOU', 'MDW-PHX', 'MDW-LAS',
                'HOU-BWI', 'HOU-MDW', 'HOU-PHX', 'HOU-LAS',
                'PHX-BWI', 'PHX-MDW', 'PHX-HOU', 'PHX-LAS'
            ]
        },
        'B6': {  # JetBlue Airways
            'name': 'JetBlue Airways',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/JetBlue_Airways_Logo.svg/200px-JetBlue_Airways_Logo.svg.png',
            'description': 'Low-cost carrier with focus on East Coast',
            'hub_routes': ['JFK', 'BOS', 'FLL', 'MCO', 'LGB'],
            'typical_routes': [
                'JFK-BOS', 'JFK-FLL', 'JFK-MCO', 'JFK-LGB',
                'BOS-JFK', 'BOS-FLL', 'BOS-MCO',
                'FLL-JFK', 'FLL-BOS', 'FLL-MCO',
                'MCO-JFK', 'MCO-BOS', 'MCO-FLL'
            ]
        },
        'US': {  # US Airways (merged with American in 2015)
            'name': 'US Airways',
            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/US_Airways_logo_2012.svg/200px-US_Airways_logo_2012.svg.png',
            'description': 'Major US airline (merged with American Airlines in 2015)',
            'hub_routes': ['PHL', 'CLT', 'PHX', 'PIT'],
            'typical_routes': [
                'PHL-CLT', 'PHL-PHX', 'PHL-PIT',
                'CLT-PHL', 'CLT-PHX', 'CLT-PIT',
                'PHX-PHL', 'PHX-CLT', 'PHX-PIT'
            ]
        }
    }
    
    return airline_routes

def map_routes_to_airlines(route_frequencies: Dict, airline_routes: Dict) -> Dict:
    """Map actual routes to airlines based on frequency and typical routes"""
    
    route_to_airline = {}
    
    for route, frequency in route_frequencies.items():
        source, destination = route.split('-')
        
        # Score each airline based on how well they match this route
        airline_scores = {}
        
        for airline_code, airline_data in airline_routes.items():
            score = 0
            
            # Check if this is a typical route for this airline
            if route in airline_data['typical_routes']:
                score += 10
            
            # Check if source or destination is a hub for this airline
            if source in airline_data['hub_routes']:
                score += 5
            if destination in airline_data['hub_routes']:
                score += 5
            
            # Bonus for high-frequency routes (more likely to be major airline)
            if frequency > 100:
                score += 3
            elif frequency > 50:
                score += 2
            elif frequency > 20:
                score += 1
            
            airline_scores[airline_code] = score
        
        # Assign the airline with the highest score
        if airline_scores:
            best_airline = max(airline_scores, key=airline_scores.get)
            if airline_scores[best_airline] > 0:
                route_to_airline[route] = best_airline
    
    return route_to_airline

def generate_airline_data():
    """Generate complete airline mapping data"""
    
    # Parse flight data
    print("📊 Parsing flight data...")
    routes = parse_flights_file('Data/flights.metta')
    
    # Analyze patterns
    print("🔍 Analyzing route patterns...")
    analysis = analyze_route_patterns(routes)
    
    # Create airline mapping
    print("✈️ Creating airline mapping...")
    airline_routes = create_airline_mapping()
    
    # Map routes to airlines
    print("🗺️ Mapping routes to airlines...")
    route_to_airline = map_routes_to_airlines(analysis['route_frequencies'], airline_routes)
    
    # Create final data structure
    airline_data = {
        'metadata': {
            'total_flights': analysis['total_flights'],
            'unique_routes': analysis['unique_routes'],
            'mapped_routes': len(route_to_airline),
            'coverage_percentage': round((len(route_to_airline) / analysis['unique_routes']) * 100, 2)
        },
        'airlines': airline_routes,
        'route_mapping': route_to_airline,
        'top_routes': analysis['top_routes'][:20]  # Top 20 routes
    }
    
    # Save to files
    print("💾 Saving airline data...")
    
    with open('airline_mapping.json', 'w') as f:
        json.dump(airline_data, f, indent=2)
    
    # Create summary
    with open('airline_summary.txt', 'w') as f:
        f.write("AIRLINE MAPPING SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total flights analyzed: {analysis['total_flights']:,}\n")
        f.write(f"Unique routes found: {analysis['unique_routes']:,}\n")
        f.write(f"Routes mapped to airlines: {len(route_to_airline):,}\n")
        f.write(f"Coverage: {airline_data['metadata']['coverage_percentage']}%\n\n")
        
        f.write("TOP 10 ROUTES:\n")
        for i, (route, count) in enumerate(analysis['top_routes'][:10], 1):
            airline = route_to_airline.get(route, 'Unknown')
            f.write(f"{i:2d}. {route}: {count:,} flights ({airline})\n")
        
        f.write("\nAIRLINE BREAKDOWN:\n")
        airline_counts = Counter(route_to_airline.values())
        for airline_code, count in airline_counts.most_common():
            airline_name = airline_routes[airline_code]['name']
            f.write(f"{airline_code}: {airline_name} - {count:,} routes\n")
    
    print("✅ Airline mapping complete!")
    print(f"📈 Coverage: {airline_data['metadata']['coverage_percentage']}%")
    print(f"📁 Files created: airline_mapping.json, airline_summary.txt")
    
    return airline_data

if __name__ == "__main__":
    generate_airline_data() 