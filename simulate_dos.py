import time
from scapy.all import IP, UDP, send

# --- Configuration ---
# !!! WARNING: ONLY use an IP address on your own local network for testing !!!
target_ip = "127.0.0.1"
# Common UDP ports are 53 (DNS), 123 (NTP), 161 (SNMP)
target_port = 53
packet_count = 1000
# Delay in seconds between sending each packet
delay = 0.001

# --- Script ---
print(f"🚀 Simulating UDP flood with {packet_count} packets to {target_ip}:{target_port}")

try:
    for i in range(packet_count):
        # Craft the UDP packet
        packet = IP(dst=target_ip) / UDP(dport=target_port)
        # Send the packet
        send(packet, verbose=False)
        time.sleep(delay)

    print(f"\n✅ Simulation complete. Sent {packet_count} packets.")

except PermissionError:
    print("\n[!] Permission Error: This script requires administrator privileges to send packets.")
    print("    Please close this window and re-run the script from a Command Prompt or PowerShell with 'Run as administrator'.")
except OSError as e:
    print(f"\n[!] Network Error: {e}")
    print("    This can happen if Npcap is not installed or the network interface is down.")
    print("    Please ensure Npcap is installed correctly (see instructions below).")