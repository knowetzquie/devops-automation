# convert_json_to_yaml.py
import json
import yaml
# Read JSON file
with open('network_devices.json', 'r') as file:
 json_data = json.load(file)
# Convert to YAML
with open('network_devices.yaml', 'w') as file:
 yaml.dump(json_data, file, default_flow_style=False, indent=2)
print("Converted network_devices.json to network_devices.yaml")