#!/usr/bin/env python3
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from modules.utils import print_color, GREEN, RED
from modules.network import get_network_info, check_internet
from modules.interface import get_original_mac, change_mac_address, change_interface_state
from modules.scanner import send_udp_probe, monitor_arp_cache

def scan_and_change_mac():
    try:
        # Steps 1-2: Get network information including gateway and interface
        local_ip, network_prefix, gateway, interface = get_network_info()
        print_color(f"Current interface: {interface}", GREEN)
        print_color(f"Gateway: {gateway}", GREEN)
        print_color(f"Scanning network {network_prefix}.0/24...", GREEN)
        
        # Store original MAC for recovery
        original_mac = get_original_mac(interface)
        if not original_mac:
            print_color("Could not get original MAC address", RED)
            sys.exit(1)
        
        # Clear ARP cache
        os.system('ip neigh flush all >/dev/null 2>&1')
        
        # Steps 3-4: Scan for MAC addresses
        devices = {}
        with ThreadPoolExecutor(max_workers=1) as monitor_executor:
            monitor_future = monitor_executor.submit(monitor_arp_cache, 2.0, gateway)
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                ips_to_scan = [
                    f"{network_prefix}.{i}" for i in range(1, 255)
                    if f"{network_prefix}.{i}" != gateway
                ]
                list(executor.map(
                    lambda ip: send_udp_probe(ip, devices),
                    ips_to_scan
                ))
            
            found_devices = monitor_future.result()
        
        # Steps 5-6: Check if devices were found
        if not found_devices:
            print_color("No MAC addresses found!", RED)
            sys.exit(1)
        
        mac_addresses = [mac for _, mac in found_devices]
        print_color(f"\nFound {len(mac_addresses)} MAC addresses to try", GREEN)
        
        # Steps 7-11: Try each MAC address
        attempts = 0
        while mac_addresses:
            attempts += 1
            # Step 7: Shut down interface
            print_color(f"\nAttempt {attempts}/{len(mac_addresses) + attempts - 1}", GREEN)
            print_color("Shutting down interface...", GREEN)
            if not change_interface_state(interface, "down"):
                continue
            
            # Step 8: Change MAC address
            new_mac = mac_addresses.pop(0)
            print_color(f"Changing MAC to: {new_mac}", GREEN)
            if not change_mac_address(interface, new_mac):
                continue
            
            # Step 9: Start interface
            print_color("Starting interface...", GREEN)
            if not change_interface_state(interface, "up"):
                continue
            
            # Give interface time to come up
            time.sleep(2)
            
            # Step 10: Check internet connection
            if check_internet():
                print_color("Successfully connected to internet!", GREEN)
                sys.exit(0)
            else:
                print_color("Failed to connect with current MAC", RED)
        
        # If we get here, all MACs failed
        print_color("\nAll MAC addresses failed to connect", RED)
        
        # Restore original MAC
        print_color("Restoring original MAC address...", GREEN)
        change_interface_state(interface, "down")
        change_mac_address(interface, original_mac)
        change_interface_state(interface, "up")
            
    except Exception as e:
        print_color(f"Error: {e}", RED)
    except KeyboardInterrupt:
        print_color("\nOperation interrupted by user", RED)
        # Restore original MAC
        change_interface_state(interface, "down")
        change_mac_address(interface, original_mac)
        change_interface_state(interface, "up")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print_color("This script requires root privileges. Please run with sudo.", RED)
        sys.exit(1)
    
    start_time = time.time()
    scan_and_change_mac()
    end_time = time.time()
    print_color(f"\nScan completed in {end_time - start_time:.2f} seconds", GREEN)
