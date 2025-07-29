#!/usr/bin/env python3
"""
Generate Multi-Airline Complete Mapping
Creates a comprehensive airline mapping with multiple airlines per route and realistic frequencies
"""

import re
import json
import random
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

def get_multi_airline_for_route(route: str) -> Dict:
    """Get multiple airlines for a route with realistic frequency distribution"""
    source, destination = route.split('-')
    
    # Major route patterns with realistic airline competition
    major_routes = {
        # Transcontinental routes (high competition)
        'JFK-LAX': {
            'airlines': ['AA', 'DL', 'UA', 'B6'],
            'frequencies': {'AA': 0.35, 'DL': 0.25, 'UA': 0.25, 'B6': 0.15}
        },
        'LAX-JFK': {
            'airlines': ['AA', 'DL', 'UA', 'B6'],
            'frequencies': {'AA': 0.35, 'DL': 0.25, 'UA': 0.25, 'B6': 0.15}
        },
        'JFK-SFO': {
            'airlines': ['AA', 'UA', 'DL', 'B6'],
            'frequencies': {'AA': 0.30, 'UA': 0.35, 'DL': 0.20, 'B6': 0.15}
        },
        'SFO-JFK': {
            'airlines': ['AA', 'UA', 'DL', 'B6'],
            'frequencies': {'AA': 0.30, 'UA': 0.35, 'DL': 0.20, 'B6': 0.15}
        },
        'EWR-LAX': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.45, 'AA': 0.35, 'DL': 0.20}
        },
        'LAX-EWR': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.45, 'AA': 0.35, 'DL': 0.20}
        },
        'EWR-SFO': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.50, 'AA': 0.30, 'DL': 0.20}
        },
        'SFO-EWR': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.50, 'AA': 0.30, 'DL': 0.20}
        },
        
        # Hub-to-hub routes
        'JFK-ATL': {
            'airlines': ['DL', 'AA', 'B6'],
            'frequencies': {'DL': 0.50, 'AA': 0.30, 'B6': 0.20}
        },
        'ATL-JFK': {
            'airlines': ['DL', 'AA', 'B6'],
            'frequencies': {'DL': 0.50, 'AA': 0.30, 'B6': 0.20}
        },
        'EWR-ORD': {
            'airlines': ['UA', 'AA'],
            'frequencies': {'UA': 0.60, 'AA': 0.40}
        },
        'ORD-EWR': {
            'airlines': ['UA', 'AA'],
            'frequencies': {'UA': 0.60, 'AA': 0.40}
        },
        'LGA-ATL': {
            'airlines': ['DL', 'AA', 'WN'],
            'frequencies': {'DL': 0.45, 'AA': 0.35, 'WN': 0.20}
        },
        'ATL-LGA': {
            'airlines': ['DL', 'AA', 'WN'],
            'frequencies': {'DL': 0.45, 'AA': 0.35, 'WN': 0.20}
        },
        'LGA-ORD': {
            'airlines': ['AA', 'UA', 'WN'],
            'frequencies': {'AA': 0.40, 'UA': 0.35, 'WN': 0.25}
        },
        'ORD-LGA': {
            'airlines': ['AA', 'UA', 'WN'],
            'frequencies': {'AA': 0.40, 'UA': 0.35, 'WN': 0.25}
        },
        
        # Florida routes (high competition)
        'JFK-MIA': {
            'airlines': ['AA', 'DL', 'B6'],
            'frequencies': {'AA': 0.40, 'DL': 0.35, 'B6': 0.25}
        },
        'MIA-JFK': {
            'airlines': ['AA', 'DL', 'B6'],
            'frequencies': {'AA': 0.40, 'DL': 0.35, 'B6': 0.25}
        },
        'JFK-MCO': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.35, 'B6': 0.35, 'DL': 0.30}
        },
        'MCO-JFK': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.35, 'B6': 0.35, 'DL': 0.30}
        },
        'JFK-FLL': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.30, 'B6': 0.40, 'DL': 0.30}
        },
        'FLL-JFK': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.30, 'B6': 0.40, 'DL': 0.30}
        },
        'EWR-MIA': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.40, 'AA': 0.35, 'DL': 0.25}
        },
        'MIA-EWR': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.40, 'AA': 0.35, 'DL': 0.25}
        },
        'EWR-MCO': {
            'airlines': ['UA', 'AA', 'B6'],
            'frequencies': {'UA': 0.35, 'AA': 0.35, 'B6': 0.30}
        },
        'MCO-EWR': {
            'airlines': ['UA', 'AA', 'B6'],
            'frequencies': {'UA': 0.35, 'AA': 0.35, 'B6': 0.30}
        },
        'EWR-FLL': {
            'airlines': ['UA', 'B6', 'AA'],
            'frequencies': {'UA': 0.30, 'B6': 0.40, 'AA': 0.30}
        },
        'FLL-EWR': {
            'airlines': ['UA', 'B6', 'AA'],
            'frequencies': {'UA': 0.30, 'B6': 0.40, 'AA': 0.30}
        },
        'LGA-MIA': {
            'airlines': ['AA', 'DL', 'B6'],
            'frequencies': {'AA': 0.40, 'DL': 0.35, 'B6': 0.25}
        },
        'MIA-LGA': {
            'airlines': ['AA', 'DL', 'B6'],
            'frequencies': {'AA': 0.40, 'DL': 0.35, 'B6': 0.25}
        },
        'LGA-MCO': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.35, 'B6': 0.35, 'DL': 0.30}
        },
        'MCO-LGA': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.35, 'B6': 0.35, 'DL': 0.30}
        },
        'LGA-FLL': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.30, 'B6': 0.40, 'DL': 0.30}
        },
        'FLL-LGA': {
            'airlines': ['AA', 'B6', 'DL'],
            'frequencies': {'AA': 0.30, 'B6': 0.40, 'DL': 0.30}
        },
        
        # Texas routes
        'JFK-DFW': {
            'airlines': ['AA', 'DL'],
            'frequencies': {'AA': 0.60, 'DL': 0.40}
        },
        'DFW-JFK': {
            'airlines': ['AA', 'DL'],
            'frequencies': {'AA': 0.60, 'DL': 0.40}
        },
        'LGA-DFW': {
            'airlines': ['AA', 'DL'],
            'frequencies': {'AA': 0.60, 'DL': 0.40}
        },
        'DFW-LGA': {
            'airlines': ['AA', 'DL'],
            'frequencies': {'AA': 0.60, 'DL': 0.40}
        },
        'EWR-DFW': {
            'airlines': ['UA', 'AA'],
            'frequencies': {'UA': 0.55, 'AA': 0.45}
        },
        'DFW-EWR': {
            'airlines': ['UA', 'AA'],
            'frequencies': {'UA': 0.55, 'AA': 0.45}
        },
        'JFK-IAH': {
            'airlines': ['AA', 'UA'],
            'frequencies': {'AA': 0.50, 'UA': 0.50}
        },
        'IAH-JFK': {
            'airlines': ['AA', 'UA'],
            'frequencies': {'AA': 0.50, 'UA': 0.50}
        },
        'EWR-IAH': {
            'airlines': ['UA', 'AA'],
            'frequencies': {'UA': 0.60, 'AA': 0.40}
        },
        'IAH-EWR': {
            'airlines': ['UA', 'AA'],
            'frequencies': {'UA': 0.60, 'AA': 0.40}
        },
        
        # Other major routes
        'JFK-BOS': {
            'airlines': ['B6', 'AA', 'DL'],
            'frequencies': {'B6': 0.45, 'AA': 0.30, 'DL': 0.25}
        },
        'BOS-JFK': {
            'airlines': ['B6', 'AA', 'DL'],
            'frequencies': {'B6': 0.45, 'AA': 0.30, 'DL': 0.25}
        },
        'EWR-BOS': {
            'airlines': ['UA', 'B6', 'AA'],
            'frequencies': {'UA': 0.40, 'B6': 0.35, 'AA': 0.25}
        },
        'BOS-EWR': {
            'airlines': ['UA', 'B6', 'AA'],
            'frequencies': {'UA': 0.40, 'B6': 0.35, 'AA': 0.25}
        },
        'LGA-BOS': {
            'airlines': ['B6', 'AA', 'DL'],
            'frequencies': {'B6': 0.50, 'AA': 0.30, 'DL': 0.20}
        },
        'BOS-LGA': {
            'airlines': ['B6', 'AA', 'DL'],
            'frequencies': {'B6': 0.50, 'AA': 0.30, 'DL': 0.20}
        },
        'JFK-SEA': {
            'airlines': ['DL', 'AA', 'UA'],
            'frequencies': {'DL': 0.40, 'AA': 0.35, 'UA': 0.25}
        },
        'SEA-JFK': {
            'airlines': ['DL', 'AA', 'UA'],
            'frequencies': {'DL': 0.40, 'AA': 0.35, 'UA': 0.25}
        },
        'EWR-SEA': {
            'airlines': ['UA', 'DL', 'AA'],
            'frequencies': {'UA': 0.45, 'DL': 0.35, 'AA': 0.20}
        },
        'SEA-EWR': {
            'airlines': ['UA', 'DL', 'AA'],
            'frequencies': {'UA': 0.45, 'DL': 0.35, 'AA': 0.20}
        },
        'JFK-DEN': {
            'airlines': ['AA', 'UA', 'DL'],
            'frequencies': {'AA': 0.35, 'UA': 0.40, 'DL': 0.25}
        },
        'DEN-JFK': {
            'airlines': ['AA', 'UA', 'DL'],
            'frequencies': {'AA': 0.35, 'UA': 0.40, 'DL': 0.25}
        },
        'EWR-DEN': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.50, 'AA': 0.30, 'DL': 0.20}
        },
        'DEN-EWR': {
            'airlines': ['UA', 'AA', 'DL'],
            'frequencies': {'UA': 0.50, 'AA': 0.30, 'DL': 0.20}
        },
        'LGA-DEN': {
            'airlines': ['AA', 'UA', 'DL'],
            'frequencies': {'AA': 0.40, 'UA': 0.35, 'DL': 0.25}
        },
        'DEN-LGA': {
            'airlines': ['AA', 'UA', 'DL'],
            'frequencies': {'AA': 0.40, 'UA': 0.35, 'DL': 0.25}
        },
    }
    
    # Check if it's a major route first
    if route in major_routes:
        return major_routes[route]
    
    # Generate realistic multi-airline patterns for other routes
    source_airlines = {
        'JFK': ['AA', 'DL', 'B6'],
        'LGA': ['AA', 'DL', 'B6', 'WN'],
        'EWR': ['UA', 'AA', 'DL'],
        'ATL': ['DL', 'AA', 'WN'],
        'ORD': ['AA', 'UA', 'WN'],
        'DFW': ['AA', 'DL'],
        'LAX': ['AA', 'UA', 'DL', 'B6'],
        'SFO': ['UA', 'AA', 'DL'],
        'DEN': ['UA', 'AA', 'DL'],
        'MIA': ['AA', 'DL', 'B6'],
        'MCO': ['AA', 'B6', 'DL'],
        'FLL': ['B6', 'AA', 'DL'],
        'BOS': ['B6', 'AA', 'DL'],
        'SEA': ['DL', 'UA', 'AA'],
        'DTW': ['DL', 'AA'],
        'MSP': ['DL', 'AA'],
        'CLT': ['AA', 'US'],
        'IAH': ['UA', 'AA'],
        'PHX': ['AA', 'US', 'WN'],
        'LAS': ['WN', 'AA', 'DL'],
    }
    
    # Get airlines for source and destination
    source_airline_list = source_airlines.get(source, ['AA', 'UA', 'DL'])
    dest_airline_list = source_airlines.get(destination, ['AA', 'UA', 'DL'])
    
    # Find common airlines
    common_airlines = list(set(source_airline_list) & set(dest_airline_list))
    
    if len(common_airlines) >= 2:
        # Multiple airlines serve both airports
        airlines = common_airlines[:3]  # Max 3 airlines
        if len(airlines) == 2:
            frequencies = {airlines[0]: 0.60, airlines[1]: 0.40}
        else:
            frequencies = {airlines[0]: 0.45, airlines[1]: 0.35, airlines[2]: 0.20}
    else:
        # Single dominant airline
        primary_airline = source_airline_list[0] if source_airline_list else 'AA'
        airlines = [primary_airline]
        frequencies = {primary_airline: 1.0}
    
    return {
        'airlines': airlines,
        'frequencies': frequencies
    }

def generate_multi_airline_complete_mapping(routes: Set[str]) -> Dict:
    """Generate complete multi-airline mapping for all routes"""
    
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
    
    # Generate route mapping with multiple airlines
    route_mapping = {}
    airline_stats = defaultdict(int)
    multi_airline_routes = 0
    
    for route in sorted(routes):
        route_info = get_multi_airline_for_route(route)
        route_mapping[route] = route_info
        
        # Count statistics
        for airline in route_info['airlines']:
            airline_stats[airline] += 1
        
        if len(route_info['airlines']) > 1:
            multi_airline_routes += 1
    
    # Generate top routes
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
            "multi_airline_routes": multi_airline_routes,
            "single_airline_routes": len(routes) - multi_airline_routes,
            "version": "4.0",
            "description": "Complete multi-airline mapping covering all routes in flights.metta with realistic competition"
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
    
    # Generate complete multi-airline mapping
    print("🔄 Generating complete multi-airline mapping...")
    mapping = generate_multi_airline_complete_mapping(routes)
    
    # Save to file
    output_file = "airline_mapping_multi_complete.json"
    with open(output_file, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"✅ Complete multi-airline mapping saved to {output_file}")
    print(f"📊 Coverage: {mapping['metadata']['mapped_routes']}/{mapping['metadata']['unique_routes']} routes ({mapping['metadata']['coverage_percentage']}%)")
    print(f"🛫 Multi-airline routes: {mapping['metadata']['multi_airline_routes']} ({mapping['metadata']['multi_airline_routes']/len(routes)*100:.1f}%)")
    print(f"✈️ Single-airline routes: {mapping['metadata']['single_airline_routes']} ({mapping['metadata']['single_airline_routes']/len(routes)*100:.1f}%)")
    
    # Print airline distribution
    print("\n📈 Airline Distribution:")
    for airline, count in mapping['airline_distribution'].items():
        percentage = (count / len(routes)) * 100
        print(f"  {airline}: {count} routes ({percentage:.1f}%)")
    
    # Show some example routes with multiple airlines
    print(f"\n🔍 Sample Multi-Airline Routes:")
    multi_airline_examples = []
    for route, route_info in mapping['route_mapping'].items():
        if len(route_info['airlines']) > 1:
            multi_airline_examples.append((route, route_info))
            if len(multi_airline_examples) >= 5:
                break
    
    for route, route_info in multi_airline_examples:
        airlines_str = ", ".join([f"{mapping['airlines'][code]['name']} ({code})" for code in route_info['airlines']])
        print(f"  {route}: {airlines_str}")

if __name__ == "__main__":
    main() 