#!/usr/bin/env python3
"""
Add MeTTa line comments to the CSV file for correlation
"""

import re
import csv

def extract_metta_flights_with_comments(file_path, num_samples=12):
    """Extract flights with original MeTTa lines as comments"""
    flights = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Match flight pattern: (flight year month day source dest cost)
                match = re.match(r'\(flight\s+(\d+)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\)', line.strip())
                if match:
                    year = int(match.group(1))
                    month = int(match.group(2))
                    day = int(match.group(3))
                    source = match.group(4)
                    destination = match.group(5)
                    cost = int(match.group(6))
                    
                    # Include the original MeTTa line as comment
                    flight = {
                        'year': year,
                        'month': month,
                        'day': day,
                        'source': source,
                        'destination': destination,
                        'cost': cost,
                        'metta_line': line.strip()
                    }
                    
                    flights.append(flight)
                    
                    # Stop after getting enough samples
                    if len(flights) >= num_samples:
                        break
        
        return flights
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def create_metta_csv_with_comments(flights, output_file):
    """Create CSV file with MeTTa data and comments"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['year', 'month', 'day', 'source', 'destination', 'cost', 'metta_line']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for flight in flights:
            writer.writerow(flight)
    
    print(f"✅ Created {output_file} with {len(flights)} MeTTa flight entries and comments")

def main():
    """Main function to create MeTTa sample CSV with comments"""
    print("🔍 Extracting MeTTa format flights with comments...")
    
    # Extract sample flights with MeTTa lines
    flights = extract_metta_flights_with_comments('extra/all_in_one.metta', 12)
    
    if flights:
        print(f"📊 Found {len(flights)} sample flights")
        
        # Create CSV file in details folder
        output_file = 'details/metta_sample_flights.csv'
        create_metta_csv_with_comments(flights, output_file)
        
        print(f"\n📋 MeTTa Sample Data with Comments:")
        for i, flight in enumerate(flights[:3], 1):
            print(f"   {i}. {flight['source']} → {flight['destination']} | ${flight['cost']} | {flight['year']}-{flight['month']}-{flight['day']}")
            print(f"      MeTTa: {flight['metta_line']}")
        
        print(f"\n📋 Summary:")
        print(f"   - Total flights: {len(flights)}")
        print(f"   - Output file: {output_file}")
        print(f"   - Format: year, month, day, source, destination, cost, metta_line")
    else:
        print("❌ No flights found")

if __name__ == "__main__":
    main() 