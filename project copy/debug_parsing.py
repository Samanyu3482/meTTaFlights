#!/usr/bin/env python3
"""
Debug script to check parsing logic
"""

from main import load_dataset, metta_serializer
from hyperon import MeTTa

def debug_parsing():
    """Debug the parsing logic"""
    
    # Load data
    metta = MeTTa()
    metta.run("!(bind! &space (new-space))")
    metta.run("!(load-ascii &space Data_new/flights.metta)")
    
    # Test a simple query
    query = '''!(match &space 
        (flight 2025 08 09 JFK LAX $cost $takeoff $landing) 
        (flight 2025 08 09 JFK LAX $cost $takeoff $landing))'''
    
    print("Running query:", query)
    result = metta.run(query)
    
    print(f"Raw result type: {type(result)}")
    print(f"Raw result: {result}")
    
    if result:
        print(f"First item type: {type(result[0]) if isinstance(result, list) and result else 'N/A'}")
        
        # Try to parse
        parsed = metta_serializer(result)
        print(f"Parsed {len(parsed)} flights")
        
        if parsed:
            print("First parsed flight:")
            print(parsed[0])
            
            # Check for empty values
            for i, flight in enumerate(parsed[:10]):
                if not flight.get('takeoff') or not flight.get('landing'):
                    print(f"Flight {i} has empty time: {flight}")

if __name__ == "__main__":
    debug_parsing() 