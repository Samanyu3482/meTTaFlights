#!/usr/bin/env python3
"""
Enhanced Airline Service for MeTTa Flight API
Provides airline information for flight routes with multiple airlines per route
"""

import json
import os
import random
from typing import Dict, Optional, List

class AirlineService:
    def __init__(self, mapping_file: str = 'airline_mapping_enhanced.json'):
        """Initialize airline service with enhanced mapping data"""
        self.mapping_file = mapping_file
        self.airline_data = None
        self.airlines = {}
        self.route_mapping = {}
        self.load_airline_data()
    
    def load_airline_data(self):
        """Load enhanced airline mapping data from JSON file"""
        try:
            if os.path.exists(self.mapping_file):
                with open(self.mapping_file, 'r') as f:
                    self.airline_data = json.load(f)
                    self.airlines = self.airline_data.get('airlines', {})
                    self.route_mapping = self.airline_data.get('route_mapping', {})
                print(f"✅ Loaded enhanced airline data: {len(self.airlines)} airlines, {len(self.route_mapping)} routes")
            else:
                print(f"⚠️ Enhanced airline mapping file not found: {self.mapping_file}")
                # Fallback to old format if enhanced file doesn't exist
                self._load_fallback_data()
        except Exception as e:
            print(f"❌ Error loading enhanced airline data: {e}")
            self._load_fallback_data()
    
    def _load_fallback_data(self):
        """Load fallback data from original airline mapping file"""
        fallback_file = 'airline_mapping_enhanced.json'
        if not os.path.exists(fallback_file):
            fallback_file = 'airline_mapping.json'
        try:
            if os.path.exists(fallback_file):
                with open(fallback_file, 'r') as f:
                    fallback_data = json.load(f)
                    self.airlines = fallback_data.get('airlines', {})
                    # Convert old format to new format
                    old_route_mapping = fallback_data.get('route_mapping', {})
                    self.route_mapping = {}
                    for route, airline_code in old_route_mapping.items():
                        self.route_mapping[route] = {
                            "airlines": [airline_code],
                            "frequencies": {airline_code: 1.0}
                        }
                print(f"✅ Loaded fallback airline data: {len(self.airlines)} airlines, {len(self.route_mapping)} routes")
            else:
                print(f"❌ No airline mapping files found")
                self.airline_data = {'airlines': {}, 'route_mapping': {}}
        except Exception as e:
            print(f"❌ Error loading fallback data: {e}")
            self.airline_data = {'airlines': {}, 'route_mapping': {}}
    
    def get_airline_for_route(self, source: str, destination: str) -> Optional[Dict]:
        """Get airline information for a specific route with weighted random selection"""
        route = f"{source}-{destination}"
        route_info = self.route_mapping.get(route)
        
        if not route_info:
            return None
        
        # Handle both old and new format
        if isinstance(route_info, str):
            # Old format - single airline
            airline_code = route_info
            if airline_code in self.airlines:
                airline_info = self.airlines[airline_code].copy()
                airline_info['code'] = airline_code
                return airline_info
        elif isinstance(route_info, dict):
            # New format - multiple airlines with frequencies
            airlines = route_info.get('airlines', [])
            frequencies = route_info.get('frequencies', {})
            
            if not airlines:
                return None
            
            # Select airline based on frequency weights
            selected_airline = self._select_airline_by_frequency(airlines, frequencies)
            
            if selected_airline and selected_airline in self.airlines:
                airline_info = self.airlines[selected_airline].copy()
                airline_info['code'] = selected_airline
                return airline_info
        
        return None
    
    def _select_airline_by_frequency(self, airlines: List[str], frequencies: Dict[str, float]) -> Optional[str]:
        """Select an airline based on frequency weights using weighted random selection"""
        if not airlines:
            return None
        
        if len(airlines) == 1:
            return airlines[0]
        
        # Create weighted choices
        choices = []
        weights = []
        
        for airline in airlines:
            weight = frequencies.get(airline, 1.0 / len(airlines))  # Default equal weight
            choices.append(airline)
            weights.append(weight)
        
        # Normalize weights to sum to 1
        total_weight = sum(weights)
        if total_weight > 0:
            normalized_weights = [w / total_weight for w in weights]
        else:
            # Equal weights if all frequencies are 0
            normalized_weights = [1.0 / len(airlines)] * len(airlines)
        
        # Select airline using weighted random choice
        try:
            selected_airline = random.choices(choices, weights=normalized_weights, k=1)[0]
            return selected_airline
        except Exception as e:
            print(f"Error in weighted selection: {e}")
            # Fallback to simple random choice
            return random.choice(airlines)
    
    def get_all_airlines_for_route(self, source: str, destination: str) -> List[Dict]:
        """Get all airlines that operate on a specific route"""
        route = f"{source}-{destination}"
        route_info = self.route_mapping.get(route)
        
        if not route_info:
            return []
        
        airlines_list = []
        
        if isinstance(route_info, str):
            # Old format - single airline
            airline_code = route_info
            if airline_code in self.airlines:
                airline_info = self.airlines[airline_code].copy()
                airline_info['code'] = airline_code
                airlines_list.append(airline_info)
        elif isinstance(route_info, dict):
            # New format - multiple airlines
            airlines = route_info.get('airlines', [])
            frequencies = route_info.get('frequencies', {})
            
            for airline_code in airlines:
                if airline_code in self.airlines:
                    airline_info = self.airlines[airline_code].copy()
                    airline_info['code'] = airline_code
                    airline_info['frequency'] = frequencies.get(airline_code, 0.0)
                    airlines_list.append(airline_info)
        
        return airlines_list
    
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
        for route, route_info in self.route_mapping.items():
            if isinstance(route_info, str):
                # Old format
                if route_info == airline_code:
                    routes.append(route)
            elif isinstance(route_info, dict):
                # New format
                airlines = route_info.get('airlines', [])
                if airline_code in airlines:
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
    
    def get_route_competition_info(self, source: str, destination: str) -> Dict:
        """Get detailed competition information for a route"""
        route = f"{source}-{destination}"
        route_info = self.route_mapping.get(route)
        
        if not route_info:
            return {"route": route, "airlines": [], "competition_level": "none"}
        
        airlines_list = self.get_all_airlines_for_route(source, destination)
        
        # Determine competition level
        if len(airlines_list) == 0:
            competition_level = "none"
        elif len(airlines_list) == 1:
            competition_level = "monopoly"
        elif len(airlines_list) == 2:
            competition_level = "duopoly"
        elif len(airlines_list) <= 4:
            competition_level = "competitive"
        else:
            competition_level = "highly_competitive"
        
        return {
            "route": route,
            "airlines": airlines_list,
            "competition_level": competition_level,
            "airline_count": len(airlines_list)
        }

# Global airline service instance
airline_service = AirlineService()

def get_airline_for_route(source: str, destination: str) -> Optional[Dict]:
    """Convenience function to get airline for a route"""
    return airline_service.get_airline_for_route(source, destination)

def get_all_airlines_for_route(source: str, destination: str) -> List[Dict]:
    """Convenience function to get all airlines for a route"""
    return airline_service.get_all_airlines_for_route(source, destination)

def get_airline_by_code(airline_code: str) -> Optional[Dict]:
    """Convenience function to get airline by code"""
    return airline_service.get_airline_by_code(airline_code)

def get_all_airlines() -> List[Dict]:
    """Convenience function to get all airlines"""
    return airline_service.get_all_airlines()

def get_route_competition_info(source: str, destination: str) -> Dict:
    """Convenience function to get route competition info"""
    return airline_service.get_route_competition_info(source, destination)

if __name__ == "__main__":
    # Test the enhanced airline service
    print("🧪 Testing Enhanced Airline Service...")
    
    # Test route mapping with multiple airlines
    test_routes = [
        ("JFK", "LAX"),
        ("EWR", "ORD"),
        ("LGA", "ATL"),
        ("JFK", "BOS"),
        ("XXX", "YYY")  # Non-existent route
    ]
    
    for source, destination in test_routes:
        print(f"\n✈️ Route: {source}-{destination}")
        
        # Get single airline (weighted random)
        airline = get_airline_for_route(source, destination)
        if airline:
            print(f"  Selected: {airline['name']} ({airline['code']})")
        else:
            print(f"  No airline found")
        
        # Get all airlines for route
        all_airlines = get_all_airlines_for_route(source, destination)
        if all_airlines:
            print(f"  All airlines: {', '.join([f'{a['name']} ({a['code']})' for a in all_airlines])}")
        
        # Get competition info
        competition = get_route_competition_info(source, destination)
        print(f"  Competition: {competition['competition_level']} ({competition.get('airline_count', 0)} airlines)")
    
    # Test airline statistics
    stats = airline_service.get_airline_statistics()
    print(f"\n📊 Statistics: {stats}")
    
    # Test airline search
    search_results = airline_service.search_airlines("American")
    print(f"\n🔍 Search 'American': {len(search_results)} results")
    for airline in search_results:
        print(f"  - {airline['name']} ({airline['code']})") 