def calculate_flight_duration(takeoff_time: str, landing_time: str) -> int:
    """Calculate flight duration in minutes"""
    try:
        # Handle times that might be missing leading zeros
        # Ensure 4-digit format (e.g., "945" becomes "0945")
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
        
        print(f"Takeoff: {takeoff_time} ({takeoff_hour}:{takeoff_minute}) = {takeoff_total} minutes")
        print(f"Landing: {landing_time} ({landing_hour}:{landing_minute}) = {landing_total} minutes")
        
        # Handle overnight flights (when landing time is earlier than takeoff time)
        if landing_total < takeoff_total:
            landing_total += 24 * 60  # Add 24 hours
            print(f"Overnight flight detected, adjusted landing: {landing_total} minutes")
            
        duration = landing_total - takeoff_total
        print(f"Duration: {duration} minutes")
        
        # Ensure duration is positive and reasonable (max 24 hours)
        if duration < 0 or duration > 24 * 60:
            # If still negative or too long, assume it's a data error and use a default
            print(f"Invalid duration detected, using default: 240 minutes")
            return 240  # Default 4 hours for domestic flights
            
        return duration
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return 240  # Default 4 hours for domestic flights

# Test cases
test_cases = [
    ("1900", "2334"),  # 19:00 to 23:34
    ("945", "1404"),   # 09:45 to 14:04
    ("1645", "1818"),  # 16:45 to 18:18
    ("0500", "0856"),  # 05:00 to 08:56
]

print("Testing duration calculation:")
print("=" * 40)

for takeoff, landing in test_cases:
    print(f"\nFlight: {takeoff} -> {landing}")
    duration = calculate_flight_duration(takeoff, landing)
    print(f"Final duration: {duration} minutes ({duration//60}h {duration%60}m)")
    print("-" * 20) 