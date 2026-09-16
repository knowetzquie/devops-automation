# json_reader.py
import json
# Read JSON file
with open('network_devices.json', 'r') as file:
 data = json.load(file)
# Access data
print("Network Devices:")
print("=" * 50)
for device in data['devices']:
 print(f"Name: {device['name']}")
 print(f"Type: {device['type']}")
 print(f"IP: {device['ip']}")
 print(f"Status: {device['status']}")
 print(f"Interfaces: {', '.join(device['interfaces'])}")
 print("-" * 50)