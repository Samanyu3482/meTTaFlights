

from hyperon import MeTTa, ExpressionAtom
import os
import glob
from datetime import datetime, timedelta

metta = MeTTa()
metta.run("!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
        
    paths = []
    if os.path.isfile(path) and path.endswith(".metta"):
        paths.append(path)
    else:
        paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    
    for file_path in paths:
        try:
            metta.run(f"!(load-ascii &space {file_path})")
        except Exception as e:
            raise Exception(f"Error loading '{file_path}': {e}")

def calculate_flight_duration(takeoff_time: str, landing_time: str) -> int:
    """Calculate flight duration in minutes"""
    try:
        # Handle empty or invalid times
        if not takeoff_time or not landing_time:
            return 240  # Default 4 hours for domestic flights
        
        # Ensure times have at least 4 digits
        takeoff_time = takeoff_time.zfill(4)
        landing_time = landing_time.zfill(4)
        
        # Parse times in HHMM format (e.g., "1645" = 16:45)
        takeoff_hour = int(takeoff_time[:2])
        takeoff_minute = int(takeoff_time[2:])
        landing_hour = int(landing_time[:2])
        landing_minute = int(landing_time[2:])
        
        # Convert to minutes since midnight
        takeoff_total = takeoff_hour * 60 + takeoff_minute
        landing_total = landing_hour * 60 + landing_minute
        
        # Handle overnight flights (when landing time is earlier than takeoff time)
        if landing_total < takeoff_total:
            landing_total += 24 * 60  # Add 24 hours
            
        duration = landing_total - takeoff_total
        
        # Ensure duration is positive and reasonable (max 24 hours)
        if duration < 0 or duration > 24 * 60:
            # If still negative or too long, assume it's a data error and use a default
            return 240  # Default 4 hours for domestic flights
            
        return duration
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return 240  # Default 4 hours for domestic flights

def parse_time_to_minutes(time_str: str) -> int:
    """Convert time string (HHMM) to minutes since midnight"""
    try:
        time_str = time_str.zfill(4)
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        return hour * 60 + minute
    except:
        return 0

def is_valid_connection(outbound_flight: dict, inbound_flight: dict, min_layover_hours: int = 1, max_layover_hours: int = 8) -> bool:
    """
    Check if two flights can form a valid connection
    - outbound_flight: First flight (source -> connection)
    - inbound_flight: Second flight (connection -> destination)
    - min_layover_hours: Minimum layover time (default 1 hour)
    - max_layover_hours: Maximum layover time (default 8 hours)
    """
    try:
        # Check if flights connect at the same airport
        if outbound_flight['destination'] != inbound_flight['source']:
            return False
        
        # Parse landing time of outbound flight
        outbound_landing = parse_time_to_minutes(outbound_flight['landing'])
        
        # Parse takeoff time of inbound flight
        inbound_takeoff = parse_time_to_minutes(inbound_flight['takeoff'])
        
        # Calculate layover time
        if inbound_takeoff < outbound_landing:
            # Overnight layover
            layover_minutes = (24 * 60 - outbound_landing) + inbound_takeoff
        else:
            # Same day layover
            layover_minutes = inbound_takeoff - outbound_landing
        
        layover_hours = layover_minutes / 60
        
        # Check if layover is within acceptable range
        return min_layover_hours <= layover_hours <= max_layover_hours
        
    except Exception as e:
        print(f"Error validating connection: {e}")
        return False

def create_connection_flight(outbound_flight: dict, inbound_flight: dict) -> dict:
    """Create a connecting flight record from two individual flights"""
    try:
        # Calculate total cost
        total_cost = int(outbound_flight['cost']) + int(inbound_flight['cost'])
        
        # Calculate total duration (flight time + layover)
        outbound_landing = parse_time_to_minutes(outbound_flight['landing'])
        inbound_takeoff = parse_time_to_minutes(inbound_flight['takeoff'])
        
        if inbound_takeoff < outbound_landing:
            # Overnight layover
            layover_minutes = (24 * 60 - outbound_landing) + inbound_takeoff
        else:
            # Same day layover
            layover_minutes = inbound_takeoff - outbound_landing
        
        total_duration = outbound_flight['duration'] + layover_minutes + inbound_flight['duration']
        
        # Calculate layover time
        layover_hours = layover_minutes / 60
        
        return {
            "year": outbound_flight['year'],
            "month": outbound_flight['month'],
            "day": outbound_flight['day'],
            "source": outbound_flight['source'],
            "destination": inbound_flight['destination'],
            "cost": str(total_cost),
            "takeoff": outbound_flight['takeoff'],
            "landing": inbound_flight['landing'],
            "duration": int(total_duration),
            "is_connecting": True,
            "connection_airport": outbound_flight['destination'],
            "layover_hours": round(layover_hours, 1),
            "segments": [
                {
                    "source": outbound_flight['source'],
                    "destination": outbound_flight['destination'],
                    "takeoff": outbound_flight['takeoff'],
                    "landing": outbound_flight['landing'],
                    "duration": outbound_flight['duration'],
                    "cost": outbound_flight['cost']
                },
                {
                    "source": inbound_flight['source'],
                    "destination": inbound_flight['destination'],
                    "takeoff": inbound_flight['takeoff'],
                    "landing": inbound_flight['landing'],
                    "duration": inbound_flight['duration'],
                    "cost": inbound_flight['cost']
                }
            ]
        }
    except Exception as e:
        print(f"Error creating connection flight: {e}")
        return None

def find_connecting_flights(source: str, destination: str, year: int, month: int, day: int, priority: str = "cost") -> list:
    """
    Find connecting flights using MeTTa pattern matching and Python logic
    """
    try:
        # Use MeTTa to get all flights for the given date
        all_flights_query = f'''!(match &space
            (flight {year} {month:02d} {day:02d} $src $dest $cost $takeoff $landing)
            (flight {year} {month:02d} {day:02d} $src $dest $cost $takeoff $landing))'''
        
        all_flights_result = metta.run(all_flights_query)
        all_flights = metta_serializer(all_flights_result)
        
        if not all_flights:
            return []
        
        # Find outbound flights (from source to any airport)
        outbound_flights = [f for f in all_flights if f['source'] == source]
        
        # Find inbound flights (from any airport to destination)
        inbound_flights = [f for f in all_flights if f['destination'] == destination]
        
        # Find valid connections
        connections = []
        for outbound in outbound_flights:
            for inbound in inbound_flights:
                if is_valid_connection(outbound, inbound):
                    connection = create_connection_flight(outbound, inbound)
                    if connection:
                        connections.append(connection)
        
        # Sort connections based on priority
        if priority == "cost":
            connections = sorted(connections, key=lambda x: int(x['cost']))
        elif priority == "time":
            connections = sorted(connections, key=lambda x: x['duration'])
        elif priority == "optimized":
            if connections:
                # Find min and max values for normalization
                min_cost = min(int(c['cost']) for c in connections)
                max_cost = max(int(c['cost']) for c in connections)
                min_duration = min(c['duration'] for c in connections)
                max_duration = max(c['duration'] for c in connections)
                
                # Avoid division by zero
                cost_range = max_cost - min_cost if max_cost != min_cost else 1
                duration_range = max_duration - min_duration if max_duration != min_duration else 1
                
                def combined_score(connection):
                    # Normalize cost and duration to 0-1 range
                    normalized_cost = (int(connection['cost']) - min_cost) / cost_range
                    normalized_duration = (connection['duration'] - min_duration) / duration_range
                    
                    # Combined score (lower is better) - average of both
                    return (normalized_cost + normalized_duration) / 2
                
                connections = sorted(connections, key=combined_score)
        
        return connections
        
    except Exception as e:
        print(f"Error finding connecting flights: {e}")
        return []

def metta_serializer(metta_result):
    result = []
    if not metta_result:
        return result
    
    data_to_process = metta_result
    if isinstance(metta_result, list) and len(metta_result) > 0:
        data_to_process = metta_result[0] if isinstance(metta_result[0], list) else metta_result
    
    for item in data_to_process:
        if isinstance(item, ExpressionAtom):
            expr = item.get_children()
            if len(expr) >= 9 and str(expr[0]) == "flight":  # New format has 9 parts
                takeoff_time = str(expr[7])
                landing_time = str(expr[8])
                duration = calculate_flight_duration(takeoff_time, landing_time)
                
                result.append({
                    "year": str(expr[1]),
                    "month": str(expr[2]),
                    "day": str(expr[3]),
                    "source": str(expr[4]),
                    "destination": str(expr[5]),
                    "cost": str(expr[6]),
                    "takeoff": takeoff_time,
                    "landing": landing_time,
                    "duration": duration
                })
        elif hasattr(item, '__str__'):
            item_str = str(item)
            if item_str.startswith("(flight "):
                parts = item_str.strip("()").split()
                if len(parts) >= 9:  # New format has 9 parts
                    takeoff_time = parts[7]
                    landing_time = parts[8]
                    duration = calculate_flight_duration(takeoff_time, landing_time)
                    
                    result.append({
                        "year": parts[1],
                        "month": parts[2],
                        "day": parts[3],
                        "source": parts[4],
                        "destination": parts[5],
                        "cost": parts[6],
                        "takeoff": takeoff_time,
                        "landing": landing_time,
                        "duration": duration
                    })
    
    return result

def search_flights(source=None, destination=None, year=None, month=None, day=None, priority="cost"):
    """Search flights using direct match queries with priority-based sorting"""
    
    # Build the pattern based on provided parameters
    src_pattern = source if source else "$src"
    dest_pattern = destination if destination else "$dest"
    year_pattern = year if year else "$year"
    month_pattern = month if month else "$month"
    day_pattern = day if day else "$day"
    
    query = f'''!(match &space 
        (flight {year_pattern} {month_pattern} {day_pattern} {src_pattern} {dest_pattern} $cost $takeoff $landing) 
        (flight {year_pattern} {month_pattern} {day_pattern} {src_pattern} {dest_pattern} $cost $takeoff $landing))'''
    
    try:
        result = metta.run(query)
        parsed_results = metta_serializer(result)
        
        # Sort based on priority
        if priority == "cost":
            return sorted(parsed_results, key=lambda x: int(x['cost']))
        elif priority == "time":
            return sorted(parsed_results, key=lambda x: x['duration'])
        elif priority == "optimized":
            # Combined optimization: normalize cost and time, then sort by combined score
            if not parsed_results:
                return parsed_results
                
            # Find min and max values for normalization
            min_cost = min(int(f['cost']) for f in parsed_results)
            max_cost = max(int(f['cost']) for f in parsed_results)
            min_duration = min(f['duration'] for f in parsed_results)
            max_duration = max(f['duration'] for f in parsed_results)
            
            # Avoid division by zero
            cost_range = max_cost - min_cost if max_cost != min_cost else 1
            duration_range = max_duration - min_duration if max_duration != min_duration else 1
            
            def combined_score(flight):
                # Normalize cost and duration to 0-1 range
                normalized_cost = (int(flight['cost']) - min_cost) / cost_range
                normalized_duration = (flight['duration'] - min_duration) / duration_range
                
                # Combined score (lower is better) - average of both
                return (normalized_cost + normalized_duration) / 2
            
            return sorted(parsed_results, key=combined_score)
        else:
            # Default to cost sorting
            return sorted(parsed_results, key=lambda x: int(x['cost']))
            
    except Exception as e:
        print(f"Search error: {e}")
        return []


def search_by_source(source, priority="cost"):
    """Search flights by source airport only"""
    return search_flights(source=source, priority=priority)

def search_by_destination(destination, priority="cost"):
    """Search flights by destination airport only"""
    return search_flights(destination=destination, priority=priority)

def search_by_date(year, month, day, priority="cost"):
    """Search flights by date only"""
    return search_flights(year=year, month=month, day=day, priority=priority)

def search_by_route(source, destination, priority="cost"):
    """Search flights by source and destination"""
    return search_flights(source=source, destination=destination, priority=priority)

def search_by_source_date(source, year, month, day, priority="cost"):
    """Search flights by source and date"""
    return search_flights(source=source, year=year, month=month, day=day, priority=priority)

def search_by_dest_date(destination, year, month, day, priority="cost"):
    """Search flights by destination and date"""
    return search_flights(destination=destination, year=year, month=month, day=day, priority=priority)

def search_comprehensive(source, destination, year, month, day, priority="cost"):
    """Search flights by all parameters"""
    return search_flights(source=source, destination=destination, year=year, month=month, day=day, priority=priority)

def search_all_flights(priority="cost"):
    """Get all flights"""
    return search_flights(priority=priority)

def smart_search(source=None, destination=None, year=None, month=None, day=None, priority="cost", include_connections=True):
    """
    Search with any combination of parameters, including connecting flights
    """
    # First, get direct flights
    direct_flights = search_flights(source=source, destination=destination, year=year, month=month, day=day, priority=priority)
    
    # If we have both source and destination, also look for connecting flights
    if include_connections and source and destination and year and month and day:
        connecting_flights = find_connecting_flights(source, destination, year, month, day, priority)
        
        # Combine direct and connecting flights
        all_flights = direct_flights + connecting_flights
        
        # Sort the combined results based on priority
        if priority == "cost":
            all_flights = sorted(all_flights, key=lambda x: int(x['cost']))
        elif priority == "time":
            all_flights = sorted(all_flights, key=lambda x: x['duration'])
        elif priority == "optimized":
            if all_flights:
                # Find min and max values for normalization
                min_cost = min(int(f['cost']) for f in all_flights)
                max_cost = max(int(f['cost']) for f in all_flights)
                min_duration = min(f['duration'] for f in all_flights)
                max_duration = max(f['duration'] for f in all_flights)
                
                # Avoid division by zero
                cost_range = max_cost - min_cost if max_cost != min_cost else 1
                duration_range = max_duration - min_duration if max_duration != min_duration else 1
                
                def combined_score(flight):
                    # Normalize cost and duration to 0-1 range
                    normalized_cost = (int(flight['cost']) - min_cost) / cost_range
                    normalized_duration = (flight['duration'] - min_duration) / duration_range
                    
                    # Combined score (lower is better) - average of both
                    return (normalized_cost + normalized_duration) / 2
                
                all_flights = sorted(all_flights, key=combined_score)
        
        return all_flights
    
    return direct_flights

def get_user_input_and_search():
    print("Flight Search System")
    print("=" * 20)
    
    source = input("Enter source airport (or press Enter for any): ").strip().upper()
    destination = input("Enter destination airport (or press Enter for any): ").strip().upper()
    
    year_input = input("Year (e.g., 2013): ").strip()
    month_input = input("Month (e.g., 1): ").strip()
    day_input = input("Day (e.g., 1): ").strip()
    
    source = source if source else None
    destination = destination if destination else None
    year = int(year_input) if year_input else None
    month = int(month_input) if month_input else None
    day = int(day_input) if day_input else None
    
    return smart_search(source, destination, year, month, day)

try:
    load_dataset("Data_new/flights.metta")
    print("Flight data loaded successfully!")
except Exception as e:
    print(f"Error loading files: {e}")

if __name__ == "__main__":
    flights = get_user_input_and_search()
    if(len(flights)==0):
        print("No flights found for the given criteria.")
    else:
        print(flights)