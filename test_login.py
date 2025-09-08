import requests
import json

def test_login():
    url = "https://lavenderneurons.onpella.app/api/login"
    data = {
        "email": "admin@codecraft.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ LOGIN SUCCESSFUL!")
        else:
            print("❌ LOGIN FAILED!")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_login()