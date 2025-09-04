#!/usr/bin/env python3
import requests
import json

def test_admin_login():
    """Test admin login via API"""
    try:
        # API endpoint
        url = "http://localhost:5000/api/login"
        
        # Admin credentials
        credentials = {
            "email": "admin@example.com",
            "password": "Admin123!"
        }
        
        # Make login request
        response = requests.post(url, json=credentials)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user = data.get('user', {})
                print(f"\n✅ Login successful!")
                print(f"User Name: {user.get('name')}")
                print(f"Email: {user.get('email')}")
                print(f"Is Admin: {user.get('isAdmin')}")
                print(f"Token: {data.get('token', 'N/A')}")
            else:
                print(f"\n❌ Login failed: {data.get('message')}")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error testing login: {str(e)}")

if __name__ == "__main__":
    test_admin_login()