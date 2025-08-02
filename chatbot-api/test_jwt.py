#!/usr/bin/env python3
import jwt
import os

# Test the SECRET_KEY from the chatbot APIs
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"

# Test token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU0MDEzNDE3LCJ0eXBlIjoiYWNjZXNzIn0.J6gFEnfXrzPHeR1uoJjHi22MPfcsVGwdNtVgjduppok"

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("✅ JWT token validation successful!")
    print(f"User ID: {payload.get('sub')}")
    print(f"Expires: {payload.get('exp')}")
    print(f"Type: {payload.get('type')}")
except jwt.ExpiredSignatureError:
    print("❌ Token has expired")
except jwt.PyJWTError as e:
    print(f"❌ JWT validation failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 