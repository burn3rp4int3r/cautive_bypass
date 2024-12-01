import socket
import time
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Set, Dict

def send_udp_probe(ip: str, devices: Dict[str, str]):
    """Send UDP probe to an IP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.1)
        sock.sendto(b'', (ip, 67))
        try:
            sock.recvfrom(1024)
        except socket.timeout:
            pass
        sock.close()
    except Exception:
        pass

def monitor_arp_cache(duration: float = 1.0, gateway: str = None) -> Set[tuple]:
    """Monitor ARP cache for changes, excluding gateway"""
    devices = set()
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            with open('/proc/net/arp', 'r') as f:
                next(f)  # Skip header
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 4 and parts[3] != "00:00:00:00:00:00":
                        ip, mac = parts[0], parts[3]
                        if ip != gateway and mac != "00:00:00:00:00:00":
                            devices.add((ip, mac))
        except Exception:
            pass
        time.sleep(0.1)
    
    return devices
