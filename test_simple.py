import requests

def test_backend():
    print("Testing backend connectivity...")
    
    # Test root endpoint
    try:
        response = requests.get("https://lavenderneurons.onpella.app/", timeout=10)
        print(f"Root endpoint - Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is responding")
        else:
            print("❌ Backend returned error")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test health endpoint
    try:
        response = requests.get("https://lavenderneurons.onpella.app/api/health", timeout=10)
        print(f"Health endpoint - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")

if __name__ == "__main__":
    test_backend()