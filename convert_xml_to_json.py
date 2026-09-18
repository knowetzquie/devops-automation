# convert_xml_to_json.py
import xmltodict
import json
# Read XML file
with open('network_config.xml', 'r') as file:
 xml_content = file.read()
# Parse XML to dictionary
data = xmltodict.parse(xml_content)
# Convert to JSON
with open('network_config.json', 'w') as file:
 json.dump(data, file, indent=4)
print("Converted network_config.xml to network_config.json")