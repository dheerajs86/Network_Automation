from netmiko import ConnectHandler

# Cisco device details
cisco_device = {
    'device_type': 'cisco_ios',
    'host': '10.10.20.48',       # Replace with your router IP
    'username': 'developer',         # Replace with router username
    'password': 'C1sco12345',      # Replace with router password
}

# Connect and show running config
net_connect = ConnectHandler(**cisco_device)
output = net_connect.send_command("show running-config")
print(output)

net_connect.disconnect()
