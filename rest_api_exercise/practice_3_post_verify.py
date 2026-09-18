import requests

url = "https://jsonplaceholder.typicode.com/posts"
payload = {
    "title": "Verification Post",
    "body": "Testing post creation and verification.",
    "userId": 1
}

# Step 1: Send POST request
response = requests.post(url, json=payload)

# Step 2: Verify creation
if response.status_code == 201:
    data = response.json()
    print("Status verified: 201 Created")
    
    # Check that payload fields match returned data
    if data.get("title") == payload["title"] and "id" in data:
        print(f"Verification successful! Assigned Post ID: {data['id']}")
    else:
        print("Verification failed: Payload data does not match.")
else:
    print(f"Verification failed with status code: {response.status_code}")