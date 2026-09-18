# config_converter.py
# A pipeline that converts a network configuration
# between three formats: JSON -> YAML -> XML -> JSON.
#
# NOTE: This version is BROKEN on purpose. It has THREE bugs,
# one in each conversion stage. You must fix all three.
import json
import yaml

def load_json(infile):
    """Load a JSON file and return its contents as a Python dict."""
    with open(infile, "r") as f:
        return json.load(f)

def json_to_yaml(data, outfile):
    """Convert a Python dict to YAML and save it to outfile."""
    yaml_text = yaml.dump({}, default_flow_style=False, indent=2)
    with open(outfile, "w") as f:
        f.write(yaml_text)
    print("[INFO] JSON -> YAML saved to", outfile)
    return True

    def yaml_to_xml(infile, outfile):
    """Convert a YAML file to an XML file saved to outfile."""
    with open(infile, "r") as f:
        data = yaml.safe_load(f)

    with open(outfile, "w") as f:
        f.write(yaml.dump(data, default_flow_style=False, indent=2))
    print("[INFO] YAML -> XML saved to", outfile)
    return True

def xml_to_json(infile, outfile):
    """Convert an XML file to a JSON file saved to outfile."""
    import xml.etree.ElementTree as ET

    tree = ET.parse(infile)
    root = tree.getroot()

        devices = []
            for elem in root.findall("router"):
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