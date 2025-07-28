#!/usr/bin/env python3
"""
Update Flight Years Script
Updates all flight records from 2013 to 2025 in flights.metta
"""

import os
import re
from datetime import datetime

def update_flight_years(input_file: str, output_file: str, old_year: str = "2013", new_year: str = "2025"):
    """
    Update all flight records from old_year to new_year
    
    Args:
        input_file: Path to input flights.metta file
        output_file: Path to output updated flights.metta file
        old_year: Year to replace (default: "2013")
        new_year: Year to replace with (default: "2025")
    """
    
    print(f"🔄 Updating flight years from {old_year} to {new_year}...")
    
    # Read the original file
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File {input_file} not found")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Count original records
    original_count = content.count(f"(flight {old_year}")
    print(f"📊 Found {original_count} flight records from {old_year}")
    
    # Replace all occurrences of the old year with the new year
    # Use regex to ensure we only replace the year in flight records
    pattern = rf"\(flight {old_year} "
    replacement = f"(flight {new_year} "
    
    updated_content = re.sub(pattern, replacement, content)
    
    # Count updated records
    updated_count = updated_content.count(f"(flight {new_year}")
    print(f"✅ Updated {updated_count} flight records to {new_year}")
    
    # Create backup of original file
    backup_file = f"{input_file}.backup"
    try:
        with open(backup_file, 'w') as f:
            f.write(content)
        print(f"💾 Created backup: {backup_file}")
    except Exception as e:
        print(f"⚠️ Warning: Could not create backup: {e}")
    
    # Write updated content to output file
    try:
        with open(output_file, 'w') as f:
            f.write(updated_content)
        print(f"✅ Updated file saved: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error writing updated file: {e}")
        return False

def verify_update(input_file: str, year: str = "2025"):
    """Verify that the update was successful"""
    print(f"🔍 Verifying update to {year}...")
    
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Count records with new year
        new_year_count = content.count(f"(flight {year}")
        old_year_count = content.count("(flight 2013")
        
        print(f"📊 Records with {year}: {new_year_count}")
        print(f"📊 Records with 2013: {old_year_count}")
        
        if new_year_count > 0 and old_year_count == 0:
            print("✅ Update verified successfully!")
            return True
        else:
            print("❌ Update verification failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def main():
    """Main function to update flight years"""
    
    input_file = "Data/flights.metta"
    output_file = "Data/flights_2025.metta"
    
    print("🚀 Flight Year Update Tool")
    print("=" * 40)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found")
        print("Please run this script from the project directory")
        return
    
    # Update the flight years
    success = update_flight_years(input_file, output_file, "2013", "2025")
    
    if success:
        print("\n" + "=" * 40)
        print("✅ Update completed successfully!")
        
        # Verify the update
        verify_update(output_file, "2025")
        
        print(f"\n📁 Files:")
        print(f"  Original: {input_file}")
        print(f"  Updated: {output_file}")
        print(f"  Backup: {input_file}.backup")
        
        print(f"\n🔄 Next steps:")
        print(f"  1. Review the updated file: {output_file}")
        print(f"  2. If satisfied, replace the original:")
        print(f"     mv {output_file} {input_file}")
        print(f"  3. Restart your API server to use the new data")
        
    else:
        print("❌ Update failed!")

if __name__ == "__main__":
    main() 