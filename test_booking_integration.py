#!/usr/bin/env python3
"""
Test script to verify booking functionality with backend API
"""

import requests
import json
from datetime import datetime, timedelta

# API Configuration
API_BASE_URL = "http://localhost:8001"

def test_booking_integration():
    """Test the complete booking flow"""
    
    print("🧪 Testing Booking Integration")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": "booking_test@example.com",
        "password": "testpass123",
        "name": "Booking Test User"
    }
    
    # Flight data
    tomorrow = datetime.now() + timedelta(days=1)
    flight_data = {
        "year": str(tomorrow.year),
        "month": str(tomorrow.month).zfill(2),
        "day": str(tomorrow.day).zfill(2),
        "source": "JFK",
        "destination": "LAX",
        "cost": "299",
        "takeoff": "0830",
        "landing": "1145",
        "duration": 375,
        "is_connecting": False,
        "airline": {
            "code": "DL",
            "name": "Delta Airlines",
            "logo": "/airline-logos/dl.png",
            "description": "Delta Airlines - Connecting the world"
        }
    }
    
    # Passenger data
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "passport_number": "US123456789",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "seat_preference": "window",
        "special_requests": "Vegetarian meal"
    }
    
    # Payment data
    payment_data = {
        "card_number": "4111111111111111",
        "card_holder_name": "John Doe",
        "expiry_month": "12",
        "expiry_year": "2025",
        "cvv": "123",
        "billing_address": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "country": "United States"
    }
    
    try:
        # Step 1: Register a new user
        print("1. Registering new user...")
        register_response = requests.post(
            f"{API_BASE_URL}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if register_response.status_code == 200:
            print("✅ User registered successfully")
            auth_data = register_response.json()
            access_token = auth_data["access_token"]
            user_data = auth_data["user"]
            print(f"   User ID: {user_data['id']}")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return
        
        # Step 2: Create a booking
        print("\n2. Creating a booking...")
        booking_request = {
            "flight": flight_data,
            "passengers": [passenger_data],
            "payment": payment_data,
            "passenger_count": 1
        }
        
        booking_response = requests.post(
            f"{API_BASE_URL}/api/bookings",
            json=booking_request,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if booking_response.status_code == 200:
            booking = booking_response.json()
            print("✅ Booking created successfully")
            print(f"   Booking Reference: {booking['booking_ref']}")
            print(f"   Status: {booking['status']}")
            print(f"   Total Cost: ${booking['total_cost']}")
            print(f"   Passengers: {booking['passenger_count']}")
        else:
            print(f"❌ Booking creation failed: {booking_response.status_code}")
            print(f"   Response: {booking_response.text}")
            return
        
        # Step 3: Get user bookings
        print("\n3. Getting user bookings...")
        bookings_response = requests.get(
            f"{API_BASE_URL}/api/bookings",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if bookings_response.status_code == 200:
            bookings_data = bookings_response.json()
            print("✅ User bookings retrieved successfully")
            print(f"   Total bookings: {bookings_data['total']}")
            
            if bookings_data['total'] > 0:
                latest_booking = bookings_data['bookings'][0]
                print(f"   Latest booking: {latest_booking['booking_ref']}")
                print(f"   Flight: {latest_booking['source']} → {latest_booking['destination']}")
                print(f"   Date: {latest_booking['flight_month']}/{latest_booking['flight_day']}/{latest_booking['flight_year']}")
            else:
                print("   No bookings found")
        else:
            print(f"❌ Failed to get bookings: {bookings_response.status_code}")
            return
        
        # Step 4: Get upcoming bookings
        print("\n4. Getting upcoming bookings...")
        upcoming_response = requests.get(
            f"{API_BASE_URL}/api/bookings/upcoming",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if upcoming_response.status_code == 200:
            upcoming_data = upcoming_response.json()
            print("✅ Upcoming bookings retrieved successfully")
            print(f"   Upcoming bookings: {upcoming_data['total']}")
        else:
            print(f"❌ Failed to get upcoming bookings: {upcoming_response.status_code}")
        
        # Step 5: Get specific booking by ID
        print("\n5. Getting specific booking...")
        booking_id = booking['id']
        specific_booking_response = requests.get(
            f"{API_BASE_URL}/api/bookings/{booking_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if specific_booking_response.status_code == 200:
            specific_booking = specific_booking_response.json()
            print("✅ Specific booking retrieved successfully")
            print(f"   Booking Reference: {specific_booking['booking_ref']}")
            print(f"   Passengers: {len(specific_booking['passengers'])}")
            print(f"   Payment: {specific_booking['payment']['card_holder_name']}")
        else:
            print(f"❌ Failed to get specific booking: {specific_booking_response.status_code}")
        
        # Step 6: Update booking status
        print("\n6. Updating booking status...")
        status_update_response = requests.put(
            f"{API_BASE_URL}/api/bookings/{booking_id}/status",
            json={"status": "cancelled"},
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if status_update_response.status_code == 200:
            updated_booking = status_update_response.json()
            print("✅ Booking status updated successfully")
            print(f"   New status: {updated_booking['status']}")
        else:
            print(f"❌ Failed to update booking status: {status_update_response.status_code}")
        
        # Step 7: Test logout and login to verify persistence
        print("\n7. Testing logout and login...")
        logout_response = requests.post(
            f"{API_BASE_URL}/api/auth/logout",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if logout_response.status_code == 200:
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed: {logout_response.status_code}")
        
        # Login again
        login_response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            new_auth_data = login_response.json()
            new_access_token = new_auth_data["access_token"]
            
            # Check if bookings are still there
            verify_bookings_response = requests.get(
                f"{API_BASE_URL}/api/bookings",
                headers={
                    "Authorization": f"Bearer {new_access_token}",
                    "Content-Type": "application/json"
                }
            )
            
            if verify_bookings_response.status_code == 200:
                verify_data = verify_bookings_response.json()
                print(f"✅ Bookings persisted after login: {verify_data['total']} bookings found")
                
                if verify_data['total'] > 0:
                    print("🎉 Booking persistence test PASSED!")
                else:
                    print("⚠️  No bookings found after login")
            else:
                print(f"❌ Failed to verify bookings after login: {verify_bookings_response.status_code}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server")
        print("   Make sure the authentication server is running on http://localhost:8001")
        print("   Run: cd backend && python api.py")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_booking_integration() 