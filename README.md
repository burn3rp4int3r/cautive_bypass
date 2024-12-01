# Cautive Bypass 
by: x.x
     '
     U

Cautive portal bypass with MAC spoofing attack

## How it works

This tools do a network device scan by an ARP request after clean the ARP cache to ensure fresh data, then change the MAC address of the current interface and verify the internet connection with the new MAC address, if it fails retry wit a new MAC address or restore the original MAC address.


## Setup

### Requirements

- Python 3.10+
- Linux OS
- Root access

I Recommend using a venv

### Environment

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate
```

## Usage

```bash
# Run the script as root
python3 main.py
```

