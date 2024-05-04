import scapy.all as scapy
from collections import Counter
from scapy.all import sniff
import socket

# List of IP addresses of websites to block
blocked_ip_list = []

# Load IP addresses of blocked websites from a file
def load_blocked_ips(filename):
    with open(filename, "r") as file:
        for line in file:
            url, _ = line.strip().split(",")
            try:
                ip_address = socket.gethostbyname(url)
                blocked_ip_list.append(ip_address)
            except socket.gaierror:
                pass  # Ignore if DNS resolution fails

# Custom action function to block packets
def block_packets(packet):
    for pkt in packet:
        ip_dst = pkt[0][1].dst
        if ip_dst in blocked_ip_list:
            # Drop the packet
            return None

# Main function
def main():
    # Load blocked IP addresses
    load_blocked_ips("websites.txt")

    # Setup sniff to capture packets
    sniff(filter="ip", prn=block_packets)

if __name__ == "__main__":
    main()