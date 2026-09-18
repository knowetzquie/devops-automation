# api_headers.py
import requests
# Custom headers
headers = {
 'Authorization': 'Bearer your-token-here',
 'Content-Type': 'application/json',
 'Accept': 'application/json',
 'User-Agent': 'DevOps-Automation/1.0'
}
# GET request with headers
response = requests.get(
 'https://jsonplaceholder.typicode.com/posts/1',
 headers=headers
)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")