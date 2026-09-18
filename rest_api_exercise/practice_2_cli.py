import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: python practice_2_cli.py <post_id>")
        sys.exit(1)

    post_id = sys.argv[1]
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        post = response.json()
        print(f"\n--- Post #{post['id']} ---")
        print(f"Title: {post['title']}")
        print(f"Body:  {post['body']}\n")
    else:
        print(f"Error: Could not find post #{post_id} (Status: {response.status_code})")

if __name__ == "__main__":
    main()