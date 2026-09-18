# api_put.py
import requests
import json
# Update an existing post
updated_post = {
 "id": 1,
 "title": "Updated Title",
 "body": "This is the updated content.",
 "userId": 1
}
# Send PUT request
response = requests.put(
 'https://jsonplaceholder.typicode.com/posts/1',
 json=updated_post,
 headers={'Content-Type': 'application/json'}
)
if response.status_code == 200:
    result = response.json()
    print("Post updated successfully!")
    print(f"Title: {result['title']}")
else:
    print(f"Failed to update post: {response.status_code}")