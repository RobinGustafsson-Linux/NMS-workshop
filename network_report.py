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
with open("network_report.txt", "w", encoding="utf-8") as report:
    report.write("=" * 80 + "\n")
    report.write(f"NÄTVERKSRAPPORT - {company}\n")
    report.write("=" * 80 + "\n")
    report.write(f"rapportdatum: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n") # current date and time .strftime to format
    report.write(f"Datauppdatering: {last_updated}\n\n")


# list comprehension to filter devices, 1 offline devices and 1 with warnings

    offline_devices = [device for device in devices if device["status"] == "offline"]
    warning_devices = [device for device in devices if device["status"] == "warning"]

    report.write("ENHETER MED PROBLEM\n")
    report.write("-------------------\n")

# f strings to format the output

    report.write("Status: Offline\n")
    for device in offline_devices:
        report.write(f"  {device['hostname']:15} {device['ip_address']:15} {device['type']:12} {device['site']}\n")
    report.write("\n")

    report.write("Status: WARNING\n")
    for device in warning_devices:
        report.write(f"  {device['hostname']:15} {device['ip_address']:15} {device['type']:12} {device['site']} (uptime: {device['uptime_days']} dagar)\n")
    report.write("\n")
                 