# api_delete.py
import requests
# Delete a post
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
if response.status_code == 200:
    print("Post deleted successfully!")
else:
    print(f"Failed to delete post: {response.status_code}")