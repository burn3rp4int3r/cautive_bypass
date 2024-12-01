# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def print_color(message: str, color: str) -> None:
    """Print colored messages"""
    print(f"{color}{message}{RESET}")
