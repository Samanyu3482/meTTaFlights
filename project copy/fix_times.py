#!/usr/bin/env python3
"""
Script to fix time format in flights.metta file
Ensures all times have 4 digits with leading zeros
"""

import re

def fix_time_format(input_file, output_file):
    """Fix time format in flights.metta file"""
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Pattern to match flight records and capture times
    # Format: (flight YEAR MONTH DAY SRC DST COST TAKEOFF LANDING)
    pattern = r'\(flight (\d{4}) (\d{1,2}) (\d{1,2}) (\w+) (\w+) (\d+) (\d{1,4}) (\d{1,4})\)'
    
    def replace_match(match):
        year, month, day, src, dst, cost, takeoff, landing = match.groups()
        
        # Ensure month and day have 2 digits
        month = month.zfill(2)
        day = day.zfill(2)
        
        # Ensure times have 4 digits
        takeoff = takeoff.zfill(4)
        landing = landing.zfill(4)
        
        return f'(flight {year} {month} {day} {src} {dst} {cost} {takeoff} {landing})'
    
    # Replace all matches
    fixed_content = re.sub(pattern, replace_match, content)
    
    # Write to output file
    with open(output_file, 'w') as f:
        f.write(fixed_content)
    
    print(f"Fixed time format in {input_file}")
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    input_file = "Data_new/flights.metta"
    output_file = "Data_new/flights_fixed.metta"
    
    fix_time_format(input_file, output_file)
    
    # Show some examples of the fix
    print("\nExamples of fixes:")
    print("Before: (flight 2025 8 9 JFK LAX 2048 1900 2334)")
    print("After:  (flight 2025 08 09 JFK LAX 2048 1900 2334)")
    print("Before: (flight 2025 8 4 EWR MSP 7471 500 856)")
    print("After:  (flight 2025 08 04 EWR MSP 7471 0500 0856)") 