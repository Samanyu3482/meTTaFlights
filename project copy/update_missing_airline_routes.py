#!/usr/bin/env python3
"""
Update Missing Airline Routes
Identifies routes that exist in flight data but are missing from airline mapping
and adds them with appropriate airline assignments.
"""

import json
import os
import re
from typing import Set, Dict, List
from collections import defaultdict

def extract_routes_from_flights_data(flights_file: str) -> Set[str]:
    """Extract all unique routes from flights.metta file"""
    routes = set()
    
    try:
        with open(flights_file, 'r') as f:
            for line in f:
                # Match flight pattern: (flight year month day source destination ...)
                match = re.match(r'\(flight\s+\d+\s+\d+\s+\d+\s+(\w+)\s+(\w+)', line)
                if match:
                    source, destination = match.groups()
                    route = f"{source}-{destination}"
                    routes.add(route)
        
        print(f"✅ Extracted {len(routes)} unique routes from flights data")
        return routes
    except Exception as e:
        print(f"❌ Error reading flights file: {e}")
        return set()

def load_current_airline_mapping(mapping_file: str) -> Dict:
    """Load current airline mapping"""
    try:
        with open(mapping_file, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"❌ Error loading airline mapping: {e}")
        return {}

def get_airline_for_route_heuristic(route: str) -> str:
    """Determine airline for a route based on heuristics and real-world patterns"""
    source, destination = route.split('-')
    
    # Major airline hub patterns
    hub_airlines = {
        # American Airlines hubs
        'DFW': 'AA', 'ORD': 'AA', 'CLT': 'AA', 'PHX': 'AA', 'MIA': 'AA',
        # United Airlines hubs
        'EWR': 'UA', 'DEN': 'UA', 'SFO': 'UA', 'IAD': 'UA',
        # Delta hubs
        'ATL': 'DL', 'DTW': 'DL', 'MSP': 'DL', 'SLC': 'DL',
        # JetBlue hubs
        'BOS': 'B6', 'FLL': 'B6', 'MCO': 'B6', 'LGB': 'B6',
        # Southwest hubs
        'MDW': 'WN', 'BWI': 'WN', 'HOU': 'WN', 'LAS': 'WN'
    }
    
    # Specific route assignments based on real-world patterns
    route_airlines = {
        # Florida routes (major carriers)
        'MIA-TPA': 'AA', 'TPA-MIA': 'AA',
        'MIA-FLL': 'AA', 'FLL-MIA': 'AA',
        'MIA-MCO': 'AA', 'MCO-MIA': 'AA',
        'TPA-FLL': 'WN', 'FLL-TPA': 'WN',
        'TPA-MCO': 'WN', 'MCO-TPA': 'WN',
        'FLL-MCO': 'WN', 'MCO-FLL': 'WN',
        
        # New York routes
        'JFK-LGA': 'DL', 'LGA-JFK': 'DL',
        'JFK-EWR': 'UA', 'EWR-JFK': 'UA',
        'LGA-EWR': 'UA', 'EWR-LGA': 'UA',
        
        # Major transcontinental routes
        'JFK-LAX': 'AA', 'LAX-JFK': 'AA',
        'JFK-SFO': 'UA', 'SFO-JFK': 'UA',
        'EWR-LAX': 'UA', 'LAX-EWR': 'UA',
        'EWR-SFO': 'UA', 'SFO-EWR': 'UA',
        
        # Hub-to-hub routes
        'DFW-ORD': 'AA', 'ORD-DFW': 'AA',
        'DFW-CLT': 'AA', 'CLT-DFW': 'AA',
        'ATL-DTW': 'DL', 'DTW-ATL': 'DL',
        'ATL-MSP': 'DL', 'MSP-ATL': 'DL',
        'EWR-DEN': 'UA', 'DEN-EWR': 'UA',
        'SFO-DEN': 'UA', 'DEN-SFO': 'UA'
    }
    
    # Check specific route assignments first
    if route in route_airlines:
        return route_airlines[route]
    
    # Check hub-based assignments
    if source in hub_airlines:
        return hub_airlines[source]
    if destination in hub_airlines:
        return hub_airlines[destination]
    
    # Special cases for NYC airports
    if source in ['JFK', 'LGA'] and destination not in ['JFK', 'LGA', 'EWR']:
        return 'AA'  # American Airlines for NYC airports
    if source == 'EWR' and destination not in ['JFK', 'LGA', 'EWR']:
        return 'UA'  # United Airlines for Newark
    
    # Fallback to American Airlines for most other routes
    return 'AA'

def update_airline_mapping_with_missing_routes(mapping_data: Dict, missing_routes: Set[str]) -> Dict:
    """Update airline mapping with missing routes"""
    updated_mapping = mapping_data.copy()
    
    # Get existing route mapping
    route_mapping = updated_mapping.get('route_mapping', {})
    
    # Add missing routes
    for route in missing_routes:
        if route not in route_mapping:
            airline_code = get_airline_for_route_heuristic(route)
            route_mapping[route] = {
                "airlines": [airline_code],
                "frequencies": {airline_code: 1.0}
            }
            print(f"➕ Added route {route} -> {airline_code}")
    
    updated_mapping['route_mapping'] = route_mapping
    
    # Update metadata
    if 'metadata' in updated_mapping:
        metadata = updated_mapping['metadata']
        metadata['total_routes'] = len(route_mapping)
        metadata['mapped_routes'] = len(route_mapping)
        metadata['coverage_percentage'] = 100.0
        metadata['version'] = metadata.get('version', '1.0') + '.1'
        metadata['description'] = metadata.get('description', '') + ' (Updated with missing routes)'
    
    return updated_mapping

def save_updated_mapping(mapping_data: Dict, output_file: str):
    """Save updated airline mapping to file"""
    try:
        with open(output_file, 'w') as f:
            json.dump(mapping_data, f, indent=2)
        print(f"✅ Updated airline mapping saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving updated mapping: {e}")

def main():
    print("🔄 Updating Missing Airline Routes...")
    
    # File paths
    flights_file = "Data_new/flights.metta"  # Using the newer flights data
    mapping_file = "airline_mapping_multi_complete.json"
    output_file = "airline_mapping_multi_complete_updated.json"
    
    # Extract routes from flight data
    print("\n📊 Extracting routes from flight data...")
    flight_routes = extract_routes_from_flights_data(flights_file)
    
    # Load current airline mapping
    print("\n📋 Loading current airline mapping...")
    current_mapping = load_current_airline_mapping(mapping_file)
    if not current_mapping:
        print("❌ Failed to load current mapping")
        return
    
    current_routes = set(current_mapping.get('route_mapping', {}).keys())
    
    # Find missing routes
    missing_routes = flight_routes - current_routes
    
    print(f"\n📈 Route Analysis:")
    print(f"  Total routes in flight data: {len(flight_routes)}")
    print(f"  Routes in current mapping: {len(current_routes)}")
    print(f"  Missing routes: {len(missing_routes)}")
    
    if not missing_routes:
        print("✅ All routes are already mapped!")
        return
    
    # Show some missing routes
    print(f"\n🔍 Sample missing routes:")
    for i, route in enumerate(sorted(missing_routes)[:10]):
        print(f"  {route}")
    if len(missing_routes) > 10:
        print(f"  ... and {len(missing_routes) - 10} more")
    
    # Update mapping with missing routes
    print(f"\n🔄 Adding missing routes to airline mapping...")
    updated_mapping = update_airline_mapping_with_missing_routes(current_mapping, missing_routes)
    
    # Save updated mapping
    print(f"\n💾 Saving updated mapping...")
    save_updated_mapping(updated_mapping, output_file)
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"  Added {len(missing_routes)} missing routes")
    print(f"  Total routes now: {len(updated_mapping['route_mapping'])}")
    print(f"  Coverage: 100%")
    
    # Show airline distribution for new routes
    print(f"\n✈️ Airline distribution for new routes:")
    airline_counts = defaultdict(int)
    for route in missing_routes:
        airline_code = updated_mapping['route_mapping'][route]['airlines'][0]
        airline_counts[airline_code] += 1
    
    for airline_code, count in sorted(airline_counts.items()):
        airline_name = updated_mapping['airlines'][airline_code]['name']
        percentage = (count / len(missing_routes)) * 100
        print(f"  {airline_name} ({airline_code}): {count} routes ({percentage:.1f}%)")

if __name__ == "__main__":
    main() 