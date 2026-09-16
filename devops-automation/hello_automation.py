# hello_automation.py
import requests
import json
# Test NetBox connection
response = requests.get('http://localhost:8000/api/')
print(f"NetBox Status: {response.status_code}")
if response.status_code == 200:
 print("NetBox is running successfully!")
else:
 print("Failed to connect to NetBox")