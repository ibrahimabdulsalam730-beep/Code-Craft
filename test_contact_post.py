import requests

url = "https://shocking-pinkskink.onpella.app/contact"
payload = {"message": "Test message from integration test"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
