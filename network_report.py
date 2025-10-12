import json
from datetime import datetime



# to read the json file
with open("network_devices.json", "r", encoding="utf-8") as file:
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
                 
# Total devices per count 
    type_count = {} 
    for device in devices:
        device_type = device["type"]
        type_count[device_type] = type_count.get(device_type, 0) + 1

# loops through all devices and writes how many of each type there are
    report.write("STATISTIK PER ENHETSTYP\n")
    report.write("-----------------------\n")
    total_devices = len(devices)
    for device_type, count in type_count.items():
        report.write(f"{device_type:15}: {count} st\n")
    report.write(f"Totalt antal enheter: {total_devices}\n\n")

 
# Devices with low uptime < 30 days
    low_uptime_devices = [device for device in devices if device["uptime_days"] < 30]
    
    report.write("ENHETER MED LÅG UPTIME (<30 DAGAR)\n")
    report.write("----------------------------------\n")
    for device in low_uptime_devices:
        report.write(f" {device["hostname"]:15} {device["uptime_days"]} dagar {device["site"]}\n")
    report.write("\n")


# Del B
# Port usage by switches

    switches = [device for device in devices if device["type"] == "switch" and "ports" in device]
    total_ports_used = sum(device["ports"]["used"] for device in switches)
    total_ports_total = sum(device["ports"]["total"] for device in switches)
    usage_percentage = (total_ports_used / total_ports_total * 100) if total_ports_total else 0

    report.write("PORTANVÄNDNING PÅ SWITCHAR\n")
    report.write("--------------------------\n")
    report.write(f"Totalt: {total_ports_used}/{total_ports_total} portar används ({usage_percentage:.1f}%)\n\n")

# Switches with high port usage > 80%
    report.write("SWITCHAR MED HÖG PORTANVÄNDNING (>80%)\n")
    report.write("---------------------------------------\n")
    for device in switches:
        used = device["ports"]["used"] 
        total = device["ports"]["total"] 
        pct = used / total * 100 if total else 0 # percentage of used ports
        if pct > 80:    # if percentage is greater than 80% write out the report below
            report.write(f" {device["hostname"]:15} {used}/{total}  ({pct:.1f}%) {device["site"]}\n") 
    report.write("\n")

# All vlans in the network
    all_vlans = set()
    for device in devices:
        for vlan in device.get("vlans", []):
            all_vlans.add(vlan)

    report.write("VLAN ÖVERSIKT\n")
    report.write("-------------\n")
    report.write(f"Antal unika VLANs: {len(all_vlans)}\n")
    report.write(f"VLANs: {', '.join(map(str, sorted(all_vlans)))}\n\n")


# Statistics per site
    report.write("STATISTIK PER SITE\n")
    report.write("------------------\n")

    for location in locations:
        site = location["site"]
        devices_in_site = location["devices"]
        total = len(devices_in_site)
        online = len([device for device in devices_in_site if device["status"] == "online"])
        offline = len([device for device in devices_in_site if device["status"] == "offline"])
        warning = len([device for device in devices_in_site if device["status"] == "warning"])
        contact = location["contact"]


        report.write(f"{site}:\n") 
        report.write(f" Enheter: {total} (online: {online}, offline: {offline}, warning: {warning})\n")
        report.write(f" kontakt: {contact}\n\n")


    report.write("=" * 80 + "\n")
    report.write("RAPPORT SLUT\n")
    report.write("=" * 80 + "\n")

print("Rapporten har skapats: network_report.txt")
