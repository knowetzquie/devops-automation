import time
import requests

def fetch_with_retry(url, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt} of {retries}...")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    print("All retry attempts failed.")
    return None

# Test with valid URL
data = fetch_with_retry("https://jsonplaceholder.typicode.com/posts/1")
if data:
    print("Successfully retrieved post:", data["title"])