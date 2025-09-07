#!/usr/bin/env python3
import requests
import json

def test_admin_apis():
    """Test admin-specific API endpoints"""
    try:
        # First, login to get token
        login_url = "http://localhost:5000/api/login"
        credentials = {
            "email": "admin@example.com",
            "password": "Admin123!"
        }
        
        login_response = requests.post(login_url, json=credentials)
        if login_response.status_code != 200:
            print("❌ Failed to login")
            return
            
        login_data = login_response.json()
        token = login_data.get('token')
        
        if not token:
            print("❌ No token received")
            return
            
        print(f"✅ Login successful, token: {token[:20]}...")
        
        # Set up headers with token
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Test /api/users endpoint
        print("\n🔍 Testing /api/users endpoint...")
        users_response = requests.get("http://localhost:5000/api/users", headers=headers)
        print(f"Status: {users_response.status_code}")
        
        if users_response.status_code == 200:
            users_data = users_response.json()
            print(f"✅ Users endpoint working - Found {len(users_data.get('users', []))} users")
        else:
            print(f"❌ Users endpoint failed: {users_response.text}")
        
        # Test /api/stats endpoint
        print("\n📊 Testing /api/stats endpoint...")
        stats_response = requests.get("http://localhost:5000/api/stats", headers=headers)
        print(f"Status: {stats_response.status_code}")
        
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"✅ Stats endpoint working")
            print(f"Stats: {json.dumps(stats_data.get('stats', {}), indent=2)}")
        else:
            print(f"❌ Stats endpoint failed: {stats_response.text}")
            
    except Exception as e:
        print(f"Error testing admin APIs: {str(e)}")

if __name__ == "__main__":
    test_admin_apis()