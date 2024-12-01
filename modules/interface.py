import subprocess
from .utils import print_color, RED

def get_original_mac(interface: str) -> str:
    """Get original MAC address of interface"""
    try:
        with open(f'/sys/class/net/{interface}/address', 'r') as f:
            return f.read().strip()
    except Exception as e:
        print_color(f"Error getting original MAC: {e}", RED)
        return ""

def change_mac_address(interface: str, mac: str) -> bool:
    """Change MAC address of interface"""
    try:
        subprocess.check_call(['ip', 'link', 'set', interface, 'address', mac],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print_color(f"Error changing MAC: {e}", RED)
        return False

def change_interface_state(interface: str, state: str) -> bool:
    """Change interface state (up/down)"""
    try:
        subprocess.check_call(['ip', 'link', 'set', interface, state],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print_color(f"Error changing interface state: {e}", RED)
        return False
