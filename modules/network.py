import socket
import subprocess
from typing import Tuple
from .utils import print_color, RED
import sys

def get_network_info() -> Tuple[str, str, str, str]:
    """Get interface and network information"""
    try:
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Get gateway IP and interface
        output = subprocess.check_output(['ip', 'route', 'show', 'default'], universal_newlines=True)
        gateway = output.split()[2]
        interface = output.split()[4]
        
        # Get network prefix
        network_prefix = '.'.join(local_ip.split('.')[:-1])
        return local_ip, network_prefix, gateway, interface
    except Exception as e:
        print_color(f"Error getting network info: {e}", RED)
        sys.exit(1)

def check_internet() -> bool:
    """Check internet connectivity"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except Exception:
        return False
