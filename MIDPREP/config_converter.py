# config_converter.py
# A pipeline that converts a network configuration
# between three formats: JSON -> YAML -> XML -> JSON.

import json
import xml.etree.ElementTree as ET

import yaml


def load_json(infile):
    """Load a JSON file and return its contents as a Python dict."""
    with open(infile, "r") as f:
        return json.load(f)


def json_to_yaml(data, outfile):
    """Convert a Python dict to YAML and save it to outfile."""
    yaml_text = yaml.dump(data, default_flow_style=False, sort_keys=False, indent=2)
    with open(outfile, "w") as f:
        f.write(yaml_text)
    print("[INFO] JSON -> YAML saved to", outfile)
    return True


def yaml_to_xml(infile, outfile):
    """Convert a YAML file to an XML file saved to outfile."""
    with open(infile, "r") as f:
        data = yaml.safe_load(f)

    root = ET.Element("devices")

    for device in data.get("devices", []):
        device_elem = ET.SubElement(root, "device")
        for key, value in device.items():
            child = ET.SubElement(device_elem, key)
            child.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(outfile, encoding="utf-8", xml_declaration=True)
    print("[INFO] YAML -> XML saved to", outfile)
    return True


def xml_to_json(infile, outfile):
    """Convert an XML file to a JSON file saved to outfile."""
    tree = ET.parse(infile)
    root = tree.getroot()
    devices = []

    for elem in root.findall("device"):
        device = {}
        for child in elem:
            device[child.tag] = child.text
        devices.append(device)

    with open(outfile, "w") as f:
        json.dump({"devices": devices}, f, indent=4)
    print("[INFO] XML -> JSON saved to", outfile)
    return True


def main():
    data = load_json("network_config.json")
    print("[INFO] Loaded configuration from JSON")
    print("[INFO] Device count:", len(data["devices"]))
    json_to_yaml(data, "config.yaml")
    yaml_to_xml("config.yaml", "config.xml")
    xml_to_json("config.xml", "config_backup.json")

    print("[INFO] Conversion pipeline finished.")


if __name__ == "__main__":
    main()













# def yaml_to_xml(infile, outfile):
#     """Convert a YAML file to an XML file saved to outfile."""
#     with open(infile, "r") as f:
#         data = yaml.safe_load(f)

#     root = ET.Element("devices")

#     for device in data["devices"]:
#         device_elem = ET.SubElement(root, "device")
#         for key, value in device.items():
#             child = ET.SubElement(device_elem, key)
#             child.text = str(value)

#     tree = ET.ElementTree(root)
#     tree.write(outfile, encoding="utf-8", xml_declaration=True)
#     print("[INFO] YAML -> XML saved to", outfile)
#     return True