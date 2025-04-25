import os
import platform

def is_computer_active(ip="192.168.1.116"):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    return os.system(f"ping {param} 1 {ip} > /dev/null 2>&1") == 0