#!/usr/bin/env python3
"""
Test script to verify profile update functionality
"""

import requests
import json

# API Configuration
API_BASE_URL = "http://localhost:8001"

def test_profile_update():
    """Test the complete profile update flow"""
    
    print("🧪 Testing Profile Update Functionality")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": "test@example.com",
        "password": "testpass123",
        "name": "Test User"
    }
    
    profile_update_data = {
        "name": "Updated Test User",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01",
        "nationality": "US",
        "address": "123 Test Street, Test City, TC 12345",
        "emergency_contact": "Emergency Contact - +1987654321"
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
            print(f"   Name: {user_data['name']}")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return
        
        # Step 2: Get current user info
        print("\n2. Getting current user info...")
        me_response = requests.get(
            f"{API_BASE_URL}/api/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if me_response.status_code == 200:
            current_user = me_response.json()
            print("✅ Current user info retrieved")
            print(f"   Name: {current_user['name']}")
            print(f"   Phone: {current_user.get('phone', 'Not set')}")
        else:
            print(f"❌ Failed to get user info: {me_response.status_code}")
            return
        
        # Step 3: Update profile
        print("\n3. Updating profile...")
        update_response = requests.put(
            f"{API_BASE_URL}/api/auth/profile",
            json=profile_update_data,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if update_response.status_code == 200:
            updated_user = update_response.json()
            print("✅ Profile updated successfully")
            print(f"   New Name: {updated_user['name']}")
            print(f"   New Phone: {updated_user.get('phone', 'Not set')}")
            print(f"   New Address: {updated_user.get('address', 'Not set')}")
        else:
            print(f"❌ Profile update failed: {update_response.status_code}")
            print(f"   Response: {update_response.text}")
            return
        
        # Step 4: Verify the update persisted
        print("\n4. Verifying profile update persisted...")
        verify_response = requests.get(
            f"{API_BASE_URL}/api/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        if verify_response.status_code == 200:
            verified_user = verify_response.json()
            print("✅ Profile update verified")
            print(f"   Name: {verified_user['name']}")
            print(f"   Phone: {verified_user.get('phone', 'Not set')}")
            print(f"   Address: {verified_user.get('address', 'Not set')}")
            
            # Check if all fields were updated correctly
            all_correct = True
            for field, expected_value in profile_update_data.items():
                actual_value = verified_user.get(field)
                if actual_value != expected_value:
                    print(f"   ❌ {field}: expected '{expected_value}', got '{actual_value}'")
                    all_correct = False
                else:
                    print(f"   ✅ {field}: '{actual_value}'")
            
            if all_correct:
                print("\n🎉 All profile fields updated and persisted correctly!")
            else:
                print("\n⚠️  Some profile fields were not updated correctly")
        else:
            print(f"❌ Failed to verify profile update: {verify_response.status_code}")
        
        # Step 5: Test login with updated profile
        print("\n5. Testing login with updated profile...")
        login_response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            logged_in_user = login_data["user"]
            print("✅ Login successful with updated profile")
            print(f"   Name: {logged_in_user['name']}")
            print(f"   Phone: {logged_in_user.get('phone', 'Not set')}")
            print(f"   Address: {logged_in_user.get('address', 'Not set')}")
            
            # Verify profile data is still there after login
            if (logged_in_user['name'] == profile_update_data['name'] and
                logged_in_user.get('phone') == profile_update_data['phone'] and
                logged_in_user.get('address') == profile_update_data['address']):
                print("🎉 Profile data persisted correctly after login!")
            else:
                print("⚠️  Profile data was not persisted after login")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server")
        print("   Make sure the backend server is running on http://localhost:8000")
        print("   Run: cd backend && python api.py")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_profile_update() 