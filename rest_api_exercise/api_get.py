# api_get.py
import requests
import json
# Public API - JSONPlaceholder
response = requests.get('https://jsonplaceholder.typicode.com/posts')
# Check if request was successful
if response.status_code == 200:
    posts = response.json()
    print(f"Successfully fetched {len(posts)} posts")
    print("\nFirst 3 posts:")
    for post in posts[:3]:
        print(f" Title: {post['title']}")
        print(f" Body: {post['body'][:50]}...")
        print("-" * 40)
else:
 print(f"Request failed with status code: {response.status_code}")