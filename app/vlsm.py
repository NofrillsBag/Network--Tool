import math
import subprocess

host_requirements = [50, 20, 10]
target_ip = "192.168.1.17"
base_ip = "192.168.1.0"
base_cidr = 24


def hosts_to_cidr(host_count):
    total_needed = host_count + 2  # include network and broadcast
    power = math.ceil(math.log2(total_needed))
    cidr = 32 - power
    return cidr

def cidr_to_subnet_mask(cidr):
    mask_bits = '1' * cidr + '0' * (32 - cidr)
    octets = [str(int(mask_bits[i:i+8], 2)) for i in range(0, 32, 8)]
    return '.'.join(octets)

def ip_to_int(ip):
    parts = list(map(int, ip.split('.')))
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def int_to_ip(ip_int):
    return '.'.join(str((ip_int >> (8 * i)) & 255) for i in [3, 2, 1, 0])

def calculate_subnet_info(ip, cidr):
    ip_int = ip_to_int(ip)
    mask = (2**32 - 1) ^ (2**(32 - cidr) - 1)
    
    network = ip_int & mask
    broadcast = network | ~mask & 0xFFFFFFFF

    first_usable = network + 1 if cidr < 31 else network
    last_usable = broadcast - 1 if cidr < 31 else broadcast

    return {
        "network_id": int_to_ip(network),
        "broadcast": int_to_ip(broadcast),
        "first_usable": int_to_ip(first_usable),
        "last_usable": int_to_ip(last_usable)
    }


def calculate_vlsm_requirements(host_counts):
    # Sort host requirements in descending order
    host_counts.sort(reverse=True)

    vlsm_blocks = []
    for hosts in host_counts:
        # Add 2 for network and broadcast addresses
        needed = hosts + 2
        # Calculate how many bits needed (2^n >= needed)
        bits = math.ceil(math.log2(needed))
        cidr = 32 - bits
        block_size = 2 ** bits
        vlsm_blocks.append({
            'hosts': hosts,
            'cidr': cidr,
            'block_size': block_size
        })
    
    return vlsm_blocks

def assign_vlsm_blocks(base_ip, base_cidr, vlsm_blocks):
    current_ip = ip_to_int(base_ip)
    
    # Get the upper bound of the base network
    base_info = calculate_subnet_info(base_ip, base_cidr)
    end_ip = ip_to_int(base_info['broadcast'])

    assignments = []

    for block in vlsm_blocks:
        cidr = block['cidr']
        block_size = block['block_size']

        # Check if this block fits within base network
        if current_ip + block_size - 1 > end_ip:
            raise ValueError(f"Not enough space to allocate /{cidr} for {block['hosts']} hosts.")

        info = calculate_subnet_info(int_to_ip(current_ip), cidr)

        assignments.append({
            'hosts_required': block['hosts'],
            'cidr': cidr,
            'network_id': info['network_id'],
            'broadcast': info['broadcast'],
            'first_usable': info['first_usable'],
            'last_usable': info['last_usable'],
            'usable_hosts': block_size - 2
        })

        # Move to next subnet
        current_ip += block_size

    return assignments

def ip_in_base_network(ip, base_ip, base_cidr): # base ip is the network ID of the WHOLE network not seperate VLSM blocks
    ip_int = ip_to_int(ip)
    base_int = ip_to_int(base_ip)
    mask = (2**32 - 1) ^ (2**(32 - base_cidr) - 1)
    return (ip_int & mask) == (base_int & mask)

def find_ip_subnet(ip, vlsm_blocks):
    ip_int = ip_to_int(ip)
    print(f"Checking {ip} (int: {ip_int})")

    for block in vlsm_blocks:
        first = ip_to_int(block["first_usable"])
        last = ip_to_int(block["last_usable"])
        print(f"  Block: {block['network_id']} - First: {int_to_ip(first)}, Last: {int_to_ip(last)}")


        if first <= ip_int <= last:
            print("  ✅ Match found!")
            return block

    return "Not in any subnet"



host_requirements = [50, 20, 10]
vlsm_blocks = calculate_vlsm_requirements(host_requirements)
assignments = assign_vlsm_blocks("192.168.1.0", 24 ,vlsm_blocks)
'''
for i, a in enumerate(assignments, 1):
    print(f"Subnet {i}: /{a['cidr']}")
    print(f"  Required Hosts : {a['hosts_required']}")
    print(f"  Network ID     : {a['network_id']}")
    print(f"  Broadcast      : {a['broadcast']}")
    print(f"  First Usable   : {a['first_usable']}")
    print(f"  Last Usable    : {a['last_usable']}")
    print(f"  Usable Hosts   : {a['usable_hosts']}")
    print()
'''

if not ip_in_base_network(target_ip, base_ip, base_cidr):
    print("⚠️ IP is not in the base network range.")
else:
    matched_block = find_ip_subnet(target_ip, assignments)