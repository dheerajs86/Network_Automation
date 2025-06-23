from netmiko import ConnectHandler
import re
import requests

# Define the device
device = {
    'device_type': 'cisco_ios',
    'ip': '10.10.20.48',           # Replace with your router's IP
    'username': 'developer',        # Replace with actual username
    'password': 'C1sco12345'      # Replace with actual password
}

# Connect to the device
net_connect = ConnectHandler(**device)

# ======== CPU Usage ========
cpu_output = net_connect.send_command("show processes cpu | include one minute")
# Example output: "CPU utilization for five seconds: 3%/0%; one minute: 5%; five minutes: 4%"

cpu_match = re.search(r"one minute: (\d+)%", str(cpu_output))
cpu_usage = cpu_match.group(1) if cpu_match else "N/A"

# ======== Memory Usage ========
mem_output = net_connect.send_command("show processes memory | include Processor Pool Total")
# Example: "Processor Pool Total:  774434176 Used:  225235600 Free:  549198576"

mem_match = re.search(r"Total:\s+(\d+)\s+Used:\s+(\d+)\s+Free:\s+(\d+)", str(mem_output))
if mem_match:
    total_mem = int(mem_match.group(1))
    used_mem = int(mem_match.group(2))
    mem_percent = round((used_mem / total_mem) * 100, 2)
else:
    mem_percent = "N/A"

# ======== Display Results ========
print(f"CPU Usage (1 min avg): {cpu_usage}%")
print(f"Memory Usage: {mem_percent}%")

with open("device_stats.log", "a") as log_file:
    log_file.write(f"CPU Usage (1 min avg): {cpu_usage}%\n")
    log_file.write(f"Memory Usage: {mem_percent}%\n")
    log_file.write("-" * 40 + "\n")

# Optional: Send to webhook or log file
webhook_url = "https://webhook.site/a20d4bc1-f559-4963-9061-d3ce4ca14abd"

data = {
    "cpu_usage": cpu_usage,
    "memory_usage": mem_percent
}

try:
    response = requests.post(webhook_url, json=data)
    if response.status_code == 200:
        print("Successfully sent to webhook.")
    else:
        print(f"Failed to send to webhook. Status code: {response.status_code}")
except Exception as e:
    print(f"Error sending to webhook: {e}")
