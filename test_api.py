import requests
import json

# Test the new backend API
BASE_URL = "https://kelly-greenrhinoceros.onpella.app"

def test_health():
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_register():
    print("\nTesting register endpoint...")
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
        response = requests.post(f"{BASE_URL}/api/register", json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Register test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API endpoints...\n")
    
    health_ok = test_health()
    root_ok = test_root()
    register_ok = test_register()
    
    print(f"\n=== Results ===")
    print(f"Health: {'✅' if health_ok else '❌'}")
    print(f"Root: {'✅' if root_ok else '❌'}")
    print(f"Register: {'✅' if register_ok else '❌'}")