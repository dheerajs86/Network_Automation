from netmiko import ConnectHandler
import requests

device = {
    'device_type': 'cisco_ios',
    'host': '10.10.20.48',
    'username': 'developer',
    'password': 'C1sco12345'
}

net_connect = ConnectHandler(**device)
output = net_connect.send_command("show ip interface brief")
if "GigabitEthernet2" in output and "administratively down" in output:
    print("ALERT: GigabitEthernet2 is down")
    # Send webhook/email/SMS as needed
    # Send webhook alert
    webhook_url = "https://webhook.site/a20d4bc1-f559-4963-9061-d3ce4ca14abd"
    data = {
        "alert": "GigabitEthernet2",
        "router_ip": device['host'],
        "status": "administratively down"
    }

    response = requests.post(webhook_url, json=data)
    print("Webhook sent:", response.status_code)
