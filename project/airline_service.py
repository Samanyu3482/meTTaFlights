#!/usr/bin/env python3
"""
Airline Service for MeTTa Flight API
Provides airline information for flight routes
"""

import json
import os
from typing import Dict, Optional, List

class AirlineService:
    def __init__(self, mapping_file: str = 'airline_mapping.json'):
        """Initialize airline service with mapping data"""
        self.mapping_file = mapping_file
        self.airline_data = None
        self.airlines = {}
        self.route_mapping = {}
        self.load_airline_data()
    
    def load_airline_data(self):
        """Load airline mapping data from JSON file"""
        try:
            if os.path.exists(self.mapping_file):
                with open(self.mapping_file, 'r') as f:
                    self.airline_data = json.load(f)
                    self.airlines = self.airline_data.get('airlines', {})
                    self.route_mapping = self.airline_data.get('route_mapping', {})
                print(f"✅ Loaded airline data: {len(self.airlines)} airlines, {len(self.route_mapping)} routes")
            else:
                print(f"⚠️ Airline mapping file not found: {self.mapping_file}")
                self.airline_data = {'airlines': {}, 'route_mapping': {}}
        except Exception as e:
            print(f"❌ Error loading airline data: {e}")
            self.airline_data = {'airlines': {}, 'route_mapping': {}}
    
    def get_airline_for_route(self, source: str, destination: str) -> Optional[Dict]:
        """Get airline information for a specific route"""
        route = f"{source}-{destination}"
        airline_code = self.route_mapping.get(route)
        
        if airline_code and airline_code in self.airlines:
            airline_info = self.airlines[airline_code].copy()
            airline_info['code'] = airline_code
            return airline_info
        
        return None
    
    def get_airline_by_code(self, airline_code: str) -> Optional[Dict]:
        """Get airline information by airline code"""
        if airline_code in self.airlines:
            airline_info = self.airlines[airline_code].copy()
            airline_info['code'] = airline_code
            return airline_info
        return None
    
    def get_all_airlines(self) -> List[Dict]:
        """Get list of all airlines"""
        airlines = []
        for code, info in self.airlines.items():
            airline_info = info.copy()
            airline_info['code'] = code
            airlines.append(airline_info)
        return airlines
    
    def get_airline_statistics(self) -> Dict:
        """Get airline mapping statistics"""
        if self.airline_data:
            return self.airline_data.get('metadata', {})
        return {}
    
    def get_routes_for_airline(self, airline_code: str) -> List[str]:
        """Get all routes for a specific airline"""
        routes = []
        for route, code in self.route_mapping.items():
            if code == airline_code:
                routes.append(route)
        return routes
    
    def search_airlines(self, query: str) -> List[Dict]:
        """Search airlines by name or code"""
        query = query.lower()
        results = []
        
        for code, info in self.airlines.items():
            if (query in code.lower() or 
                query in info['name'].lower() or 
                query in info['description'].lower()):
                airline_info = info.copy()
                airline_info['code'] = code
                results.append(airline_info)
        
        return results

# Global airline service instance
airline_service = AirlineService()

def get_airline_for_route(source: str, destination: str) -> Optional[Dict]:
    """Convenience function to get airline for a route"""
    return airline_service.get_airline_for_route(source, destination)

def get_airline_by_code(airline_code: str) -> Optional[Dict]:
    """Convenience function to get airline by code"""
    return airline_service.get_airline_by_code(airline_code)

def get_all_airlines() -> List[Dict]:
    """Convenience function to get all airlines"""
    return airline_service.get_all_airlines()

if __name__ == "__main__":
    # Test the airline service
    print("🧪 Testing Airline Service...")
    
    # Test route mapping
    test_routes = [
        ("JFK", "LAX"),
        ("EWR", "ORD"),
        ("LGA", "ATL"),
        ("JFK", "BOS"),
        ("XXX", "YYY")  # Non-existent route
    ]
    
    for source, destination in test_routes:
        airline = get_airline_for_route(source, destination)
        if airline:
            print(f"✈️ {source}-{destination}: {airline['name']} ({airline['code']})")
        else:
            print(f"❓ {source}-{destination}: No airline found")
    
    # Test airline statistics
    stats = airline_service.get_airline_statistics()
    print(f"\n📊 Statistics: {stats}")
    
    # Test airline search
    search_results = airline_service.search_airlines("American")
    print(f"\n🔍 Search 'American': {len(search_results)} results")
    for airline in search_results:
        print(f"  - {airline['name']} ({airline['code']})") 