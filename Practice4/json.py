# json.py

# Import the json module
import json


# Open the JSON file in read mode
with open("sample-data.json", "r") as file:
    # Load JSON data into a Python dictionary
    data = json.load(file)


# Print the table title
print("Interface Status")

# Print a long line
print("=" * 90)

# Print column headers with spacing
print(f"{'DN':<60} {'Description':<20} {'Speed':<8} {'MTU':<8}")

# Print a separator line
print("-" * 90)


# Loop through each item inside "imdata"
for item in data["imdata"]:
    # Go inside l1PhysIf, then inside attributes
    attributes = item["l1PhysIf"]["attributes"]

    # Get the DN value
    dn = attributes["dn"]

    # Get the description value
    descr = attributes["descr"]

    # Get the speed value
    speed = attributes["speed"]

    # Get the MTU value
    mtu = attributes["mtu"]

    # Print one row of the table
    print(f"{dn:<60} {descr:<20} {speed:<8} {mtu:<8}")