# yaml_reader.py
import yaml
# Read YAML file
with open('ansible_inventory.yaml', 'r') as file:
 data = yaml.safe_load(file)
# Access data
print("Ansible Inventory:")
print("=" * 50)
# Access routers
print("\nRouters:")
for router in data['network']['routers']:
 print(f" - {router['name']}: {router['ip']} ({router['os']})")
# Access switches
print("\nSwitches:")
for switch in data['network']['switches']:
 print(f" - {switch['name']}: {switch['ip']}")
 if 'vlans' in switch:
 print(f" VLANs: {[v['name'] for v in switch['vlans']]}")
# Access firewalls
print("\nFirewalls:")
for fw in data['network']['firewalls']:
 print(f" - {fw['name']}: {fw['ip']} ({fw['os']})")
 print(f" Zones: {', '.join(fw['zones'])}")