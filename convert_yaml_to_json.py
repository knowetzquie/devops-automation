# convert_yaml_to_json.py
import yaml
import json
# Read YAML file
with open('ansible_inventory.yaml', 'r') as file:
 yaml_data = yaml.safe_load(file)
# Convert to JSON
with open('ansible_inventory.json', 'w') as file:
 json.dump(yaml_data, file, indent=4)
print("Converted ansible_inventory.yaml to ansible_inventory.json")
