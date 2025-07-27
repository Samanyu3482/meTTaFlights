

from hyperon import MeTTa, ExpressionAtom
import os
import glob

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
            if len(expr) >= 7 and str(expr[0]) == "flight":
                result.append({
                    "year": str(expr[1]),
                    "month": str(expr[2]),
                    "day": str(expr[3]),
                    "source": str(expr[4]),
                    "destination": str(expr[5]),
                    "cost": str(expr[6])
                })
        elif hasattr(item, '__str__'):
            item_str = str(item)
            if item_str.startswith("(flight "):
                parts = item_str.strip("()").split()
                if len(parts) >= 7:
                    result.append({
                        "year": parts[1],
                        "month": parts[2],
                        "day": parts[3],
                        "source": parts[4],
                        "destination": parts[5],
                        "cost": parts[6]
                    })
    
    return result

def search_flights(source=None, destination=None, year=None, month=None, day=None):
    """Search flights using direct match queries (since MeTTa functions aren't working)"""
    
    # Build the pattern based on provided parameters
    src_pattern = source if source else "$src"
    dest_pattern = destination if destination else "$dest"
    year_pattern = year if year else "$year"
    month_pattern = month if month else "$month"
    day_pattern = day if day else "$day"
    
    query = f'''!(match &space 
        (flight {year_pattern} {month_pattern} {day_pattern} {src_pattern} {dest_pattern} $cost) 
        (flight {year_pattern} {month_pattern} {day_pattern} {src_pattern} {dest_pattern} $cost))'''
    
    try:
        result = metta.run(query)
        parsed_results = metta_serializer(result)
        return sorted(parsed_results, key=lambda x: int(x['cost']))
    except Exception as e:
        print(f"Search error: {e}")
        return []


def search_by_source(source):
    """Search flights by source airport only"""
    return search_flights(source=source)

def search_by_destination(destination):
    """Search flights by destination airport only"""
    return search_flights(destination=destination)

def search_by_date(year, month, day):
    """Search flights by date only"""
    return search_flights(year=year, month=month, day=day)

def search_by_route(source, destination):
    """Search flights by source and destination"""
    return search_flights(source=source, destination=destination)

def search_by_source_date(source, year, month, day):
    """Search flights by source and date"""
    return search_flights(source=source, year=year, month=month, day=day)

def search_by_dest_date(destination, year, month, day):
    """Search flights by destination and date"""
    return search_flights(destination=destination, year=year, month=month, day=day)

def search_comprehensive(source, destination, year, month, day):
    """Search flights by all parameters"""
    return search_flights(source=source, destination=destination, year=year, month=month, day=day)

def search_all_flights():
    """Get all flights"""
    return search_flights()

def smart_search(source=None, destination=None, year=None, month=None, day=None):
    """Search with any combination of parameters"""
    return search_flights(source=source, destination=destination, year=year, month=month, day=day)

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
    load_dataset("Data/flights.metta")
    print("Flight data loaded successfully!")
except Exception as e:
    print(f"Error loading files: {e}")

if __name__ == "__main__":
    flights = get_user_input_and_search()
    if(len(flights)==0):
        print("No flights found for the given criteria.")
    else:
        print(flights)