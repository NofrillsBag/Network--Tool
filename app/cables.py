# cables.py

ethernet_database = [
    {
        "standard": "10Base-T",
        "speed": "10 Mbps",
        "medium": "copper",
        "category": "Category 3 or higher",
        "range": "1–100",
        "description": "Legacy Ethernet over two pairs of twisted-pair copper. Obsolete in modern networks."
    },
    {
        "standard": "100Base-TX",
        "speed": "100 Mbps",
        "medium": "copper",
        "category": "Category 5 or higher",
        "range": "1–100",
        "description": "Fast Ethernet using two pairs of Cat 5 or better."
    },
    {
        "standard": "1000Base-T",
        "speed": "1 Gbps",
        "medium": "copper",
        "category": "Category 5e or higher",
        "range": "1–100",
        "description": "Gigabit Ethernet over all four pairs of Cat 5e or better. Most common wired LAN today."
    },
    {
        "standard": "1000Base-SX",
        "speed": "1 Gbps",
        "medium": "fiber",
        "category": "Multi-mode fiber (MMF)",
        "range": "220–550",
        "description": "Short-range gigabit fiber for LAN and data center use."
    },
    {
        "standard": "1000Base-LX-MMF",
        "speed": "1 Gbps",
        "medium": "fiber",
        "category": "Multi-mode fiber",
        "range": "1–550",
        "description": "Long-range gigabit fiber (MMF) for LAN and data center use."
    },
    {
        "standard": "1000Base-LX-SMF",
        "speed": "1 Gbps",
        "medium": "fiber",
        "category": "Single-mode fiber",
        "range": "1–10000",
        "description": "Long-range gigabit fiber (SMF) for campus or backbone links."
    },
    {
        "standard": "10GBase-T",
        "speed": "10 Gbps",
        "medium": "copper",
        "category": "Category 6A or higher",
        "range": "1–100",
        "description": "10 Gigabit Ethernet over twisted-pair. Requires high-quality cabling."
    },
    {
        "standard": "10GBase-SR",
        "speed": "10 Gbps",
        "medium": "fiber",
        "category": "Multi-mode fiber",
        "range": "26–400",
        "description": "Short-range 10G over fiber for data centers."
    },
    {
        "standard": "25GBase-SR",
        "speed": "25 Gbps",
        "medium": "fiber",
        "category": "Multi-mode fiber",
        "range": "70–100",
        "description": "High-speed data center uplinks over MMF."
    },
    {
        "standard": "40GBase-SR4",
        "speed": "40 Gbps",
        "medium": "fiber",
        "category": "Multi-mode fiber",
        "range": "100–150",
        "description": "Parallel fiber lanes for 40G over MMF. Used in backbones and data centers."
    },
    {
        "standard": "40GBase-T",
        "speed": "40 Gbps",
        "medium": "copper",
        "category": "Category 8",
        "range": "1–30",
        "description": "Very high-speed Ethernet over shielded twisted-pair. Data center use only."
    },
    {
        "standard": "2.5GBase-T",
        "speed": "2.5 Gbps",
        "medium": "copper",
        "category": "Category 5e or higher",
        "range": "1–100",
        "description": "Upgrade over Cat 5e cabling. Common in Wi-Fi 6 and 6E access points."
    },
    {
        "standard": "5GBase-T",
        "speed": "5 Gbps",
        "medium": "copper",
        "category": "Category 6 or higher",
        "range": "1–100",
        "description": "Bridges the gap between 1G and 10G. Popular for access switches and APs."
    },
    {
        "standard": "25GBase-T",
        "speed": "25 Gbps",
        "medium": "copper",
        "category": "Category 8",
        "range": "1–30",
        "description": "High-speed Ethernet over shielded copper. Rare outside data centers."
    },
    {
        "standard": "100GBase-SR4",
        "speed": "100 Gbps",
        "medium": "fiber",
        "category": "Multi-mode fiber (OM4/OM5)",
        "range": "70–100",
        "description": "High-speed 100G Ethernet using 4 parallel fiber pairs. Common in modern data centers."
    },
    {
        "standard": "100GBase-LR4",
        "speed": "100 Gbps",
        "medium": "fiber",
        "category": "Single-mode fiber",
        "range": "1–10000",
        "description": "Long-range 100G over single-mode fiber for WAN and metro backbone links."
    },
    {
        "standard": "100Base-FX",
        "speed": "100 Mbps",
        "medium": "fiber",
        "category": "Multi-mode fiber",
        "range": "1–2000",
        "description": "Legacy fast Ethernet over fiber. Mostly replaced by gigabit fiber."
    }
]




def lookup_by_standard(name):
    name = name.strip().lower()
    for entry in ethernet_database:
        if entry["standard"].lower() == name:
            return format_entry(entry)
    return None

def lookup_by_specs(speed, medium):
    speed = speed.strip().lower()
    medium = medium.strip().lower()
    matches = [
        format_entry(entry)
        for entry in ethernet_database
        if entry["speed"].lower() == speed and entry["medium"].lower() == medium
    ]
    return matches

def format_entry(entry):
    return {
        "Standard": entry["standard"],
        "Speed": entry["speed"],
        "Medium": entry["medium"].capitalize(),
        "Required Cable": entry["category"],
        "Range": entry["range"],
        "Description": entry["description"]
    }


def lookup_by_range(user_range, medium=None):
    results = []
    try:
        # Extract numeric value from input like "100 meters" or "300m"
        range_input = ''.join(c for c in user_range if c.isdigit())
        if not range_input:
            return []
        min_required = int(range_input)
    except:
        return []

    for entry in ethernet_database:
        try:
            # Split the standardized range like "1–100"
            min_str, max_str = entry["range"].replace("–", "-").split("-")
            min_supported = int(min_str.strip())
            max_supported = int(max_str.strip())

            # Check if the user range fits within this entry
            if min_supported <= min_required <= max_supported:
                # If medium filter is specified, apply it
                if medium and medium.lower() not in entry["medium"].lower():
                    continue
                results.append(format_entry(entry))
        except:
            continue

    return results





result = lookup_by_standard("1000Base-T")
print("🔍 Lookup result:")
for key, value in result.items():
    print(f"{key}: {value}")

result = lookup_by_specs("10 Gbps", "copper")
print("\n🔍 Lookup by specs result:")
for entry in result:
    print("\n---")
    for key, value in entry.items():
        print(f"{key}: {value}")

result = lookup_by_range("100", "copper")
print("\n🔍 Lookup by range result:")
for entry in result:
    print("\n---")
    for key, value in entry.items():
        print(f"{key}: {value}")
