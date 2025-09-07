import requests
import json

# Test the backend endpoints
BASE_URL = "https://shocking-pinkskink.onpella.app"

def test_health():
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register():
    print("\nTesting registration...")
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
        response = requests.post(f"{BASE_URL}/api/register", json=data)
        print(f"Register Status: {response.status_code}")
        print(f"Register Response: {response.json()}")
        return response.status_code in [200, 201, 400]  # 400 if user already exists
    except Exception as e:
        print(f"Registration failed: {e}")
        return False

def test_login():
    print("\nTesting login...")
    try:
        data = {
            "email": "test@example.com",
            "password": "TestPass123"
        }
        response = requests.post(f"{BASE_URL}/api/login", json=data)
        print(f"Login Status: {response.status_code}")
        print(f"Login Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Login failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend endpoints...")
    
    # Test health
    if not test_health():
        print("Backend is not healthy!")
        exit(1)
    
    # Test registration
    test_register()
    
    # Test login
    test_login()
    
    print("\nTest completed!")