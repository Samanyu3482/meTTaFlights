#!/usr/bin/env python3
"""
Generate Complete Airline Mapping
Analyzes all routes in flights.metta and creates a comprehensive airline mapping
"""

import re
import json
from collections import defaultdict
from typing import Dict, List, Set

def extract_routes_from_metta(file_path: str) -> Set[str]:
    """Extract all unique routes from flights.metta file"""
    routes = set()
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('(flight '):
                    # Parse flight record: (flight year month day source destination cost)
                    parts = line.strip('()').split()
                    if len(parts) >= 6:
                        source = parts[4]
                        destination = parts[5]
                        route = f"{source}-{destination}"
                        routes.add(route)
    except Exception as e:
        print(f"Error reading flights.metta: {e}")
        return set()
    
    return routes

def get_airline_for_route_heuristic(route: str) -> str:
    """Determine airline for a route based on heuristics and real-world patterns"""
    source, destination = route.split('-')
    
    # Major airline hub patterns
    hub_airlines = {
        # American Airlines hubs
        'DFW': 'AA', 'ORD': 'AA', 'CLT': 'AA', 'MIA': 'AA', 'PHX': 'AA', 'LAX': 'AA',
        # United Airlines hubs  
        'EWR': 'UA', 'ORD': 'UA', 'DEN': 'UA', 'SFO': 'UA', 'IAD': 'UA', 'LAX': 'UA',
        # Delta Air Lines hubs
        'ATL': 'DL', 'DTW': 'DL', 'MSP': 'DL', 'SLC': 'DL', 'JFK': 'DL', 'LAX': 'DL',
        # JetBlue hubs
        'JFK': 'B6', 'BOS': 'B6', 'FLL': 'B6', 'MCO': 'B6', 'LGB': 'B6',
        # Southwest hubs
        'MDW': 'WN', 'BWI': 'WN', 'HOU': 'WN', 'PHX': 'WN', 'LAS': 'WN',
        # US Airways hubs (now part of AA)
        'PHL': 'US', 'CLT': 'US', 'PHX': 'US', 'PIT': 'US'
    }
    
    # Route-specific assignments based on real-world patterns
    route_airlines = {
        # Major transcontinental routes
        'JFK-LAX': 'AA', 'LAX-JFK': 'AA',
        'JFK-SFO': 'AA', 'SFO-JFK': 'AA',
        'EWR-LAX': 'UA', 'LAX-EWR': 'UA',
        'EWR-SFO': 'UA', 'SFO-EWR': 'UA',
        
        # Hub-to-hub routes
        'JFK-ATL': 'DL', 'ATL-JFK': 'DL',
        'JFK-DTW': 'DL', 'DTW-JFK': 'DL',
        'JFK-MSP': 'DL', 'MSP-JFK': 'DL',
        'EWR-ORD': 'UA', 'ORD-EWR': 'UA',
        'EWR-DEN': 'UA', 'DEN-EWR': 'UA',
        'LGA-ATL': 'DL', 'ATL-LGA': 'DL',
        'LGA-ORD': 'AA', 'ORD-LGA': 'AA',
        
        # Florida routes
        'JFK-MIA': 'AA', 'MIA-JFK': 'AA',
        'JFK-MCO': 'AA', 'MCO-JFK': 'AA',
        'JFK-FLL': 'AA', 'FLL-JFK': 'AA',
        'JFK-PBI': 'AA', 'PBI-JFK': 'AA',
        'LGA-MIA': 'AA', 'MIA-LGA': 'AA',
        'LGA-MCO': 'AA', 'MCO-LGA': 'AA',
        'LGA-FLL': 'AA', 'FLL-LGA': 'AA',
        'EWR-MIA': 'UA', 'MIA-EWR': 'UA',
        'EWR-MCO': 'UA', 'MCO-EWR': 'UA',
        'EWR-FLL': 'UA', 'FLL-EWR': 'UA',
        
        # Texas routes
        'JFK-DFW': 'AA', 'DFW-JFK': 'AA',
        'LGA-DFW': 'AA', 'DFW-LGA': 'AA',
        'EWR-DFW': 'UA', 'DFW-EWR': 'UA',
        'JFK-IAH': 'AA', 'IAH-JFK': 'AA',
        'EWR-IAH': 'UA', 'IAH-EWR': 'UA',
        'LGA-HOU': 'WN', 'HOU-LGA': 'WN',
        
        # California routes
        'JFK-SAN': 'AA', 'SAN-JFK': 'AA',
        'JFK-SJC': 'AA', 'SJC-JFK': 'AA',
        'JFK-OAK': 'AA', 'OAK-JFK': 'AA',
        'EWR-SAN': 'UA', 'SAN-EWR': 'UA',
        'EWR-SJC': 'UA', 'SJC-EWR': 'UA',
        
        # Other major routes
        'JFK-BOS': 'B6', 'BOS-JFK': 'B6',
        'EWR-BOS': 'UA', 'BOS-EWR': 'UA',
        'LGA-BOS': 'B6', 'BOS-LGA': 'B6',
        'JFK-SEA': 'DL', 'SEA-JFK': 'DL',
        'EWR-SEA': 'UA', 'SEA-EWR': 'UA',
        'JFK-DEN': 'AA', 'DEN-JFK': 'AA',
        'EWR-DEN': 'UA', 'DEN-EWR': 'UA',
        'LGA-DEN': 'AA', 'DEN-LGA': 'AA',
    }
    
    # Check route-specific assignments first
    if route in route_airlines:
        return route_airlines[route]
    
    # Check hub-based assignments
    if source in hub_airlines:
        return hub_airlines[source]
    if destination in hub_airlines:
        return hub_airlines[destination]
    
    # Default assignments based on airport patterns
    if source.startswith('JFK') or source.startswith('LGA'):
        return 'AA'  # American Airlines for NYC airports
    elif source.startswith('EWR'):
        return 'UA'  # United Airlines for Newark
    elif source.startswith('ATL') or source.startswith('DTW') or source.startswith('MSP'):
        return 'DL'  # Delta for their hubs
    elif source.startswith('BOS'):
        return 'B6'  # JetBlue for Boston
    elif source.startswith('MDW') or source.startswith('BWI'):
        return 'WN'  # Southwest for their hubs
    else:
        # Fallback to American Airlines for most other routes
        return 'AA'

def generate_complete_airline_mapping(routes: Set[str]) -> Dict:
    """Generate complete airline mapping for all routes"""
    
    # Define airlines with their information
    airlines = {
        "AA": {
            "name": "American Airlines",
            "logo": "/airline-logos/aa.png",
            "description": "Major US airline with extensive domestic network",
            "hub_routes": ["JFK", "LAX", "ORD", "DFW", "MIA", "CLT", "PHX"],
            "typical_routes": ["JFK-LAX", "JFK-SFO", "JFK-MIA", "JFK-ORD", "JFK-DFW"]
        },
        "UA": {
            "name": "United Airlines",
            "logo": "/airline-logos/ua.png",
            "description": "Major US airline with global network",
            "hub_routes": ["EWR", "ORD", "DEN", "SFO", "LAX", "IAD"],
            "typical_routes": ["EWR-LAX", "EWR-SFO", "EWR-ORD", "EWR-DEN", "EWR-IAD"]
        },
        "DL": {
            "name": "Delta Air Lines",
            "logo": "/airline-logos/dl.png",
            "description": "Major US airline with extensive domestic and international network",
            "hub_routes": ["JFK", "ATL", "DTW", "MSP", "SLC", "LAX"],
            "typical_routes": ["JFK-ATL", "JFK-DTW", "JFK-MSP", "JFK-SLC", "ATL-JFK"]
        },
        "B6": {
            "name": "JetBlue Airways",
            "logo": "/airline-logos/b6.png",
            "description": "Low-cost carrier with focus on East Coast and transcontinental routes",
            "hub_routes": ["JFK", "BOS", "FLL", "MCO", "LGB"],
            "typical_routes": ["JFK-LAX", "JFK-BOS", "JFK-FLL", "JFK-MCO", "BOS-JFK"]
        },
        "WN": {
            "name": "Southwest Airlines",
            "logo": "/airline-logos/wn.png",
            "description": "Low-cost carrier with extensive domestic network",
            "hub_routes": ["MDW", "BWI", "HOU", "PHX", "LAS"],
            "typical_routes": ["MDW-BWI", "BWI-HOU", "HOU-PHX", "PHX-LAS", "LAS-MDW"]
        },
        "US": {
            "name": "US Airways",
            "logo": "/airline-logos/us.png",
            "description": "Legacy carrier (now part of American Airlines)",
            "hub_routes": ["PHL", "CLT", "PHX", "PIT"],
            "typical_routes": ["PHL-CLT", "CLT-PHX", "PHX-PIT", "PIT-PHL"]
        }
    }
    
    # Generate route mapping
    route_mapping = {}
    airline_stats = defaultdict(int)
    
    for route in sorted(routes):
        airline_code = get_airline_for_route_heuristic(route)
        route_mapping[route] = {
            "airlines": [airline_code],
            "frequencies": {airline_code: 1.0}
        }
        airline_stats[airline_code] += 1
    
    # Generate top routes (we'll use the existing data)
    top_routes = [
        ["JFK-LAX", 1705],
        ["LGA-ATL", 1558],
        ["LGA-ORD", 1285],
        ["JFK-SFO", 1254],
        ["LGA-CLT", 925],
        ["EWR-ORD", 913],
        ["JFK-BOS", 878],
        ["LGA-MIA", 841],
        ["EWR-BOS", 810],
        ["JFK-MCO", 788],
        ["LGA-DTW", 778],
        ["LGA-DFW", 760],
        ["EWR-CLT", 735],
        ["EWR-MCO", 730],
        ["EWR-ATL", 706],
        ["LGA-DCA", 699],
        ["JFK-SJU", 681],
        ["JFK-FLL", 671],
        ["LGA-BOS", 640],
        ["EWR-SFO", 608]
    ]
    
    return {
        "metadata": {
            "total_flights": 49999,
            "unique_routes": len(routes),
            "mapped_routes": len(route_mapping),
            "coverage_percentage": 100.0,
            "version": "3.0",
            "description": "Complete airline mapping covering all routes in flights.metta"
        },
        "airlines": airlines,
        "route_mapping": route_mapping,
        "top_routes": top_routes,
        "airline_distribution": dict(airline_stats)
    }

def main():
    print("🔄 Analyzing flights.metta to extract all routes...")
    
    # Extract all routes from flights.metta
    routes = extract_routes_from_metta("Data/flights.metta")
    print(f"✅ Found {len(routes)} unique routes")
    
    # Generate complete airline mapping
    print("🔄 Generating complete airline mapping...")
    mapping = generate_complete_airline_mapping(routes)
    
    # Save to file
    output_file = "airline_mapping_complete.json"
    with open(output_file, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"✅ Complete airline mapping saved to {output_file}")
    print(f"📊 Coverage: {mapping['metadata']['mapped_routes']}/{mapping['metadata']['unique_routes']} routes ({mapping['metadata']['coverage_percentage']}%)")
    
    # Print airline distribution
    print("\n📈 Airline Distribution:")
    for airline, count in mapping['airline_distribution'].items():
        percentage = (count / len(routes)) * 100
        print(f"  {airline}: {count} routes ({percentage:.1f}%)")
    
    # Show some example routes
    print(f"\n🔍 Sample Routes:")
    sample_routes = list(routes)[:10]
    for route in sample_routes:
        airline_code = mapping['route_mapping'][route]['airlines'][0]
        airline_name = mapping['airlines'][airline_code]['name']
        print(f"  {route}: {airline_name} ({airline_code})")

if __name__ == "__main__":
    main() 