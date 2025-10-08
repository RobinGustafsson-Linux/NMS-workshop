import json
from datetime import datetime


# to read the json file
with open("network_devices.json", "r") as file:
    data = json.load(file)

    company = data["company"]
    last_updated = data["last_updated"]
    locations = data["locations"] 

    devices = []
    for loc in locations:
        for dev in loc["devices"]:
            dev["site"] = loc["site"]
            dev["contact"] = loc["contact"]
            devices.append(dev)

    # Generate the report
