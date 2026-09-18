# api_error_handling.py
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout,
RequestException
def make_api_request(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise exception for bad status codes
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"An error occurred: {req_err}")

    return None
# Test with valid URL
print("Testing valid URL:")
result = make_api_request('https://jsonplaceholder.typicode.com/posts/1')
if result:
 print(f"Success: {result['title'][:30]}...")
# Test with invalid URL
print("\nTesting invalid URL:")
result = make_api_request('https://jsonplaceholder.typicode.com/nonexistent')