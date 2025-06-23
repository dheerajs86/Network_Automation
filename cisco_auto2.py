from netmiko import ConnectHandler
from datetime import datetime

# Cisco device info
cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.10.20.48',       # Replace with actual IP
    'username': 'developer',         # Replace with actual username
    'password': 'C1sco12345',      # Replace with actual password
}

# Connect to device
net_connect = ConnectHandler(**cisco_device)

# Get config and write to file
running_config = net_connect.send_command("show running-config")
filename = f"backup_running_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(filename, 'w') as f:
    f.write(running_config)
print(f"[✓] Configuration saved to {filename}")

# Create Loopback interface
commands = [
    "interface loopback0",
    "ip address 1.1.1.1 255.255.255.255",
    "description Configured by script",
    "no shutdown"
]
net_connect.send_config_set(commands)
print("[✓] Loopback0 with IP 1.1.1.1 configured.")

net_connect.disconnect()
