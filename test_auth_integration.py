#!/usr/bin/env python3
"""
Test script to verify authentication integration
"""

import requests
import json
import time

def test_auth_integration():
    """Test the authentication backend integration"""
    
    # Test URLs
    auth_base_url = "http://localhost:8001"
    flight_base_url = "http://localhost:8000"
    
    print("🧪 Testing Authentication Integration...")
    print("=" * 50)
    
    # Test 1: Check if auth backend is running
    try:
        response = requests.get(f"{auth_base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Authentication backend is running")
        else:
            print("❌ Authentication backend health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to authentication backend: {e}")
        return False
    
    # Test 2: Check if flight backend is running
    try:
        response = requests.get(f"{flight_base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Flight search backend is running")
        else:
            print("❌ Flight search backend health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to flight search backend: {e}")
        return False
    
    # Test 3: Register a new user
    print("\n📝 Testing user registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(
            f"{auth_base_url}/api/auth/register",
            json=register_data,
            timeout=10
        )
        
        if response.status_code == 200:
            auth_data = response.json()
            print("✅ User registration successful")
            print(f"   User ID: {auth_data['user']['id']}")
            print(f"   User Name: {auth_data['user']['name']}")
            print(f"   Access Token: {auth_data['access_token'][:20]}...")
            
            # Store tokens for later tests
            access_token = auth_data['access_token']
            refresh_token = auth_data['refresh_token']
            
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration request failed: {e}")
        return False
    
    # Test 4: Login with the registered user
    print("\n🔐 Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{auth_base_url}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            login_data = response.json()
            print("✅ User login successful")
            print(f"   Access Token: {login_data['access_token'][:20]}...")
            
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return False
    
    # Test 5: Get current user info with token
    print("\n👤 Testing authenticated user info...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(
            f"{auth_base_url}/api/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Authenticated user info retrieved")
            print(f"   User ID: {user_data['id']}")
            print(f"   User Name: {user_data['name']}")
            print(f"   User Email: {user_data['email']}")
            
        else:
            print(f"❌ Get user info failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Get user info request failed: {e}")
        return False
    
    # Test 6: Update user profile
    print("\n✏️ Testing profile update...")
    profile_data = {
        "name": "Updated Test User",
        "phone": "+1-555-123-4567",
        "nationality": "US"
    }
    
    try:
        response = requests.put(
            f"{auth_base_url}/api/auth/profile",
            json=profile_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            updated_user = response.json()
            print("✅ Profile update successful")
            print(f"   Updated Name: {updated_user['name']}")
            print(f"   Updated Phone: {updated_user['phone']}")
            
        else:
            print(f"❌ Profile update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Profile update request failed: {e}")
        return False
    
    # Test 7: Test logout
    print("\n🚪 Testing logout...")
    
    try:
        response = requests.post(
            f"{auth_base_url}/api/auth/logout",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Logout successful")
            
        else:
            print(f"❌ Logout failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Logout request failed: {e}")
        return False
    
    print("\n🎉 All authentication tests passed!")
    print("=" * 50)
    print("✅ Authentication backend is fully functional")
    print("✅ Frontend can now connect to the authentication system")
    print("✅ User registration, login, profile management, and logout work")
    
    return True

if __name__ == "__main__":
    print("Starting authentication integration test...")
    print("Make sure both backends are running:")
    print("  - Flight Search Backend: http://localhost:8000")
    print("  - Authentication Backend: http://localhost:8001")
    print()
    
    success = test_auth_integration()
    
    if success:
        print("\n🚀 Ready to use the full system!")
        print("Frontend: http://localhost:3000")
    else:
        print("\n❌ Some tests failed. Please check the backend services.")