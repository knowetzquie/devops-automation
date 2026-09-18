import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def make_logged_request(url):
    logging.info(f"Sending GET request to: {url}")
    try:
        response = requests.get(url, timeout=5)
        logging.info(f"Received status code: {response.status_code}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None

make_logged_request("https://jsonplaceholder.typicode.com/posts/1")
make_logged_request("https://jsonplaceholder.typicode.com/invalid-url")