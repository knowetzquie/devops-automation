# json_writer.py
import json
# Create new device data
new_device = {
 "name": "server-01",
 "type": "server",
 "ip": "192.168.1.10",
 "status": "active",
 "interfaces": ["eth0", "eth1"],
 "specs": {
 "cpu": "Intel Xeon",
 "ram": "32GB",
 "storage": "1TB SSD"
 }
}
# Write to file
with open('new_device.json', 'w') as file:
 json.dump(new_device, file, indent=4)
print("Device data written to new_device.json")