import yaml

def parse_ini_file(ini_file):
    inventory = {"all": {"hosts": {}, "children": {}}}
    current_group = None

    with open(ini_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):  # Ignore empty lines and comments
                continue

            if line.startswith("[") and line.endswith("]"):  # New group
                current_group = line[1:-1]  # Extract group name
                inventory["all"]["children"][current_group] = {"hosts": {}}
            elif current_group and " " in line:  # Host entry with variables
                parts = line.split(maxsplit=1)
                host_name = parts[0]  # First part is the hostname
                host_vars = {}

                if len(parts) > 1:  # If there are variables
                    for item in parts[1].split():
                        if "=" in item:
                            key, value = item.split("=", 1)
                            host_vars[key.strip()] = value.strip()

                inventory["all"]["children"][current_group]["hosts"][host_name] = host_vars

    return inventory

# Convert hosts.ini to inventory.yaml
ini_file = "hosts.ini"
inventory = parse_ini_file(ini_file)

# Write to inventory.yaml
yaml_file = "inventory.yaml"
with open(yaml_file, "w") as file:
    yaml.dump(inventory, file, default_flow_style=False, sort_keys=False)

print(f"Conversion complete! Check {yaml_file}")
