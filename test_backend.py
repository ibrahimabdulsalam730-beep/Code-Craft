import requests
import json

# Test your backend endpoints
BASE_URL = "https://tancentipede.onpella.app"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register():
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
        response = requests.post(f"{BASE_URL}/api/register", json=data, timeout=10)
        print(f"Register Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 201, 400]  # 400 if user exists
    except Exception as e:
        print(f"Register test failed: {e}")
        return False

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Root Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend connectivity...")
    print("=" * 50)
    
    print("\n1. Testing root endpoint...")
    test_root()
    
    print("\n2. Testing health endpoint...")
    test_health()
    
    print("\n3. Testing register endpoint...")
    test_register()
    
    print("\n" + "=" * 50)
    print("Test completed!")