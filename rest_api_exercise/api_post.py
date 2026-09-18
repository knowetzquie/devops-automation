# api_post.py
import requests
import json
# Create a new post
new_post = {
 "title": "My First API Post",
 "body": "This is the content of my post.",
 "userId": 1
}
# Send POST request
response = requests.post(
 'https://jsonplaceholder.typicode.com/posts',
 json=new_post,
 headers={'Content-Type': 'application/json'}
)
if response.status_code == 201:
    created_post = response.json()
    print("Post created successfully!")
    print(f"ID: {created_post['id']}")
    print(f"Title: {created_post['title']}")
else:
    print(f"Failed to create post: {response.status_code}")