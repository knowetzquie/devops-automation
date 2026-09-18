# xml_reader.py
import xmltodict
import json
# Read XML file
with open('network_config.xml', 'r') as file:
 xml_content = file.read()
# Parse XML to dictionary
data = xmltodict.parse(xml_content)
# Access data
print("Network Configuration:")
print("=" * 50)
# Access router
router = data['network']['router']
print(f"Router: {router['@name']}")
print(f"IP: {router['ip']}")
# Access interfaces
if 'interfaces' in router:
 print("Interfaces:")
 for iface in router['interfaces']['interface']:
    print(f" - {iface['@name']}: {iface['ip']}")
print("-" * 50)
# Access switch
switch = data['network']['switch']
print(f"Switch: {switch['@name']}")
print(f"IP: {switch['ip']}")
# Access VLANs
if 'vlans' in switch:
 print("VLANs:")
 for vlan in switch['vlans']['vlan']:
    print(f" - VLAN {vlan['@id']}: {vlan['#text']}")