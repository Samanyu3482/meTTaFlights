import json
import time
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import os

class OptimizedFlightSearch:
    def __init__(self, data_file: str = "Data_new/flights.metta"):
        self.flights = []
        self.flights_by_source = defaultdict(list)
        self.flights_by_destination = defaultdict(list)
        self.flights_by_date = defaultdict(list)
        self.flights_by_route = defaultdict(list)
        self.flights_by_source_date = defaultdict(list)
        self.flights_by_dest_date = defaultdict(list)
        self.airports = set()
        
        self.load_data(data_file)
        self.build_indexes()
    
    def load_data(self, data_file: str):
        """Load flight data from MeTTa file and parse into Python structures"""
        print(f"Loading flight data from {data_file}...")
        start_time = time.time()
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file {data_file} not found")
        
        with open(data_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or not line.startswith('(flight '):
                    continue
                
                try:
                    # Parse flight record: (flight year month day source dest cost takeoff landing)
                    parts = line.strip('()').split()
                    if len(parts) >= 9:
                        flight = {
                            'year': parts[1],
                            'month': parts[2],
                            'day': parts[3],
                            'source': parts[4],
                            'destination': parts[5],
                            'cost': str(parts[6]),  # Convert to string for frontend compatibility
                            'takeoff': parts[7],
                            'landing': parts[8],
                            'duration': self.calculate_duration(parts[7], parts[8])
                        }
                        self.flights.append(flight)
                        
                        # Track airports
                        self.airports.add(flight['source'])
                        self.airports.add(flight['destination'])
                        
                except Exception as e:
                    print(f"Error parsing line {line_num}: {e}")
                    continue
        
        load_time = time.time() - start_time
        print(f"Loaded {len(self.flights)} flights in {load_time:.2f} seconds")
    
    def build_indexes(self):
        """Build fast lookup indexes for efficient searching"""
        print("Building search indexes...")
        start_time = time.time()
        
        for flight in self.flights:
            # Index by source
            self.flights_by_source[flight['source']].append(flight)
            
            # Index by destination
            self.flights_by_destination[flight['destination']].append(flight)
            
            # Index by date (with leading zeros)
            date_key = f"{flight['year']}-{flight['month']}-{flight['day']}"
            self.flights_by_date[date_key].append(flight)
            
            # Index by route
            route_key = f"{flight['source']}-{flight['destination']}"
            self.flights_by_route[route_key].append(flight)
            
            # Index by source and date (with leading zeros)
            source_date_key = f"{flight['source']}-{flight['year']}-{flight['month']}-{flight['day']}"
            self.flights_by_source_date[source_date_key].append(flight)
            
            # Index by destination and date (with leading zeros)
            dest_date_key = f"{flight['destination']}-{flight['year']}-{flight['month']}-{flight['day']}"
            self.flights_by_dest_date[dest_date_key].append(flight)
        
        index_time = time.time() - start_time
        print(f"Built indexes in {index_time:.2f} seconds")
    
    def calculate_duration(self, takeoff: str, landing: str) -> int:
        """Calculate flight duration in minutes"""
        try:
            takeoff = takeoff.zfill(4)
            landing = landing.zfill(4)
            
            takeoff_hour = int(takeoff[:2])
            takeoff_minute = int(takeoff[2:])
            landing_hour = int(landing[:2])
            landing_minute = int(landing[2:])
            
            takeoff_total = takeoff_hour * 60 + takeoff_minute
            landing_total = landing_hour * 60 + landing_minute
            
            if landing_total < takeoff_total:
                landing_total += 24 * 60
            
            duration = landing_total - takeoff_total
            
            if duration < 0 or duration > 24 * 60:
                return 240  # Default 4 hours
            
            return duration
        except:
            return 240
    
    def search_direct_flights(self, source: Optional[str] = None, destination: Optional[str] = None, 
                            year: Optional[int] = None, month: Optional[int] = None, 
                            day: Optional[int] = None, priority: str = "cost") -> List[Dict]:
        """Search for direct flights using optimized indexes"""
        
        # Determine the most efficient search strategy
        if source and destination and year and month and day:
            # Most specific search - use source-date index and filter by destination
            source_date_key = f"{source}-{year}-{month:02d}-{day:02d}"
            matching_flights = [f for f in self.flights_by_source_date.get(source_date_key, []) 
                              if f['destination'] == destination]
            
        elif source and destination:
            # Route search
            route_key = f"{source}-{destination}"
            matching_flights = self.flights_by_route.get(route_key, [])
            
        elif source and year and month and day:
            # Source and date search
            source_date_key = f"{source}-{year}-{month:02d}-{day:02d}"
            matching_flights = self.flights_by_source_date.get(source_date_key, [])
            
        elif destination and year and month and day:
            # Destination and date search
            dest_date_key = f"{destination}-{year}-{month:02d}-{day:02d}"
            matching_flights = self.flights_by_dest_date.get(dest_date_key, [])
            
        elif source:
            # Source only search
            matching_flights = self.flights_by_source.get(source, [])
            
        elif destination:
            # Destination only search
            matching_flights = self.flights_by_destination.get(destination, [])
            
        elif year and month and day:
            # Date only search
            date_key = f"{year}-{month:02d}-{day:02d}"
            matching_flights = self.flights_by_date.get(date_key, [])
            
        else:
            # No criteria - return all flights (limited for performance)
            matching_flights = self.flights[:1000]  # Limit to prevent overwhelming results
        
        # Sort based on priority
        return self.sort_flights(matching_flights, priority)
    
    def find_connecting_flights(self, source: str, destination: str, year: int, month: int, day: int, 
                              priority: str = "cost", max_connections: int = 10) -> List[Dict]:
        """Find connecting flights using optimized approach"""
        
        date_key = f"{year}-{month:02d}-{day:02d}"
        date_flights = self.flights_by_date.get(date_key, [])
        
        if not date_flights:
            return []
        
        # Get outbound and inbound flights for the date
        outbound_flights = [f for f in date_flights if f['source'] == source]
        inbound_flights = [f for f in date_flights if f['destination'] == destination]
        
        if not outbound_flights or not inbound_flights:
            return []
        
        # Find valid connections
        connections = []
        connection_count = 0
        
        for outbound in outbound_flights:
            if connection_count >= max_connections:
                break
                
            for inbound in inbound_flights:
                if connection_count >= max_connections:
                    break
                    
                if self.is_valid_connection(outbound, inbound):
                    connection = self.create_connection_flight(outbound, inbound)
                    if connection:
                        connections.append(connection)
                        connection_count += 1
        
        return self.sort_flights(connections, priority)
    
    def is_valid_connection(self, outbound: Dict, inbound: Dict, 
                          min_layover_hours: int = 1, max_layover_hours: int = 8) -> bool:
        """Check if two flights can form a valid connection"""
        if outbound['destination'] != inbound['source']:
            return False
        
        outbound_landing = self.parse_time_to_minutes(outbound['landing'])
        inbound_takeoff = self.parse_time_to_minutes(inbound['takeoff'])
        
        if inbound_takeoff < outbound_landing:
            layover_minutes = (24 * 60 - outbound_landing) + inbound_takeoff
        else:
            layover_minutes = inbound_takeoff - outbound_landing
        
        layover_hours = layover_minutes / 60
        return min_layover_hours <= layover_hours <= max_layover_hours
    
    def create_connection_flight(self, outbound: Dict, inbound: Dict) -> Dict:
        """Create a connecting flight record"""
        total_cost = int(outbound['cost']) + int(inbound['cost'])
        
        outbound_landing = self.parse_time_to_minutes(outbound['landing'])
        inbound_takeoff = self.parse_time_to_minutes(inbound['takeoff'])
        
        if inbound_takeoff < outbound_landing:
            layover_minutes = (24 * 60 - outbound_landing) + inbound_takeoff
        else:
            layover_minutes = inbound_takeoff - outbound_landing
        
        total_duration = outbound['duration'] + layover_minutes + inbound['duration']
        layover_hours = layover_minutes / 60
        
        return {
            "year": outbound['year'],
            "month": outbound['month'],
            "day": outbound['day'],
            "source": outbound['source'],
            "destination": inbound['destination'],
            "cost": str(total_cost),  # Convert to string for frontend compatibility
            "takeoff": outbound['takeoff'],
            "landing": inbound['landing'],
            "duration": int(total_duration),
            "is_connecting": True,
            "connection_airport": outbound['destination'],
            "layover_hours": round(layover_hours, 1),
            "segments": [
                {
                    "source": outbound['source'],
                    "destination": outbound['destination'],
                    "takeoff": outbound['takeoff'],
                    "landing": outbound['landing'],
                    "duration": outbound['duration'],
                    "cost": outbound['cost']  # Already a string
                },
                {
                    "source": inbound['source'],
                    "destination": inbound['destination'],
                    "takeoff": inbound['takeoff'],
                    "landing": inbound['landing'],
                    "duration": inbound['duration'],
                    "cost": inbound['cost']  # Already a string
                }
            ]
        }
    
    def parse_time_to_minutes(self, time_str: str) -> int:
        """Convert time string (HHMM) to minutes since midnight"""
        try:
            time_str = time_str.zfill(4)
            hour = int(time_str[:2])
            minute = int(time_str[2:])
            return hour * 60 + minute
        except:
            return 0
    
    def sort_flights(self, flights: List[Dict], priority: str) -> List[Dict]:
        """Sort flights based on priority"""
        if not flights:
            return flights
        
        if priority == "cost":
            return sorted(flights, key=lambda x: int(x['cost']))
        elif priority == "time":
            return sorted(flights, key=lambda x: x['duration'])
        elif priority == "optimized":
            # Combined optimization
            min_cost = min(int(f['cost']) for f in flights)
            max_cost = max(int(f['cost']) for f in flights)
            min_duration = min(f['duration'] for f in flights)
            max_duration = max(f['duration'] for f in flights)
            
            cost_range = max_cost - min_cost if max_cost != min_cost else 1
            duration_range = max_duration - min_duration if max_duration != min_duration else 1
            
            def combined_score(flight):
                normalized_cost = (int(flight['cost']) - min_cost) / cost_range
                normalized_duration = (flight['duration'] - min_duration) / duration_range
                return (normalized_cost + normalized_duration) / 2
            
            return sorted(flights, key=combined_score)
        else:
            return sorted(flights, key=lambda x: int(x['cost']))
    
    def smart_search(self, source: Optional[str] = None, destination: Optional[str] = None,
                    year: Optional[int] = None, month: Optional[int] = None, 
                    day: Optional[int] = None, priority: str = "cost", 
                    include_connections: bool = True, limit: int = 50) -> List[Dict]:
        """Main search function with optimized performance"""
        
        start_time = time.time()
        
        # Get direct flights
        direct_flights = self.search_direct_flights(source, destination, year, month, day, priority)
        
        # Limit direct flights for performance
        direct_flights = direct_flights[:limit]
        
        # If we have both source and destination, also look for connecting flights
        if include_connections and source and destination and year and month and day:
            connecting_flights = self.find_connecting_flights(source, destination, year, month, day, priority)
            
            # Combine and sort
            all_flights = direct_flights + connecting_flights
            all_flights = self.sort_flights(all_flights, priority)
            
            # Limit total results
            all_flights = all_flights[:limit]
        else:
            all_flights = direct_flights
        
        search_time = time.time() - start_time
        print(f"Search completed in {search_time:.3f} seconds, found {len(all_flights)} flights")
        
        return all_flights
    
    def get_airports(self) -> List[str]:
        """Get list of all airports"""
        return sorted(list(self.airports))
    
    def get_stats(self) -> Dict:
        """Get search engine statistics"""
        return {
            "total_flights": len(self.flights),
            "total_airports": len(self.airports),
            "indexes_built": {
                "by_source": len(self.flights_by_source),
                "by_destination": len(self.flights_by_destination),
                "by_date": len(self.flights_by_date),
                "by_route": len(self.flights_by_route)
            }
        }

# Global instance for API use
flight_search = None

def initialize_search_engine(data_file: str = "Data_new/flights.metta"):
    """Initialize the optimized search engine"""
    global flight_search
    if flight_search is None:
        flight_search = OptimizedFlightSearch(data_file)
    return flight_search

def smart_search(source=None, destination=None, year=None, month=None, day=None, 
                priority="cost", include_connections=True):
    """Compatibility function for the existing API"""
    global flight_search
    if flight_search is None:
        flight_search = initialize_search_engine()
    
    return flight_search.smart_search(
        source=source,
        destination=destination,
        year=year,
        month=month,
        day=day,
        priority=priority,
        include_connections=include_connections
    )

def search_all_flights(priority="cost"):
    """Get all flights with limit for performance"""
    global flight_search
    if flight_search is None:
        flight_search = initialize_search_engine()
    
    return flight_search.smart_search(priority=priority, limit=100)

def load_dataset(path: str) -> None:
    """Compatibility function - initialize the search engine"""
    initialize_search_engine(path)