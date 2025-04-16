import time
import os
import json
from monitors import CpuMonitor, RamMonitor, DiskMonitor, GpuMonitor

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    cpu = CpuMonitor()
    ram = RamMonitor()
    disk = DiskMonitor()
    gpu = GpuMonitor()

    while True:
        status = {
            'cpu': cpu.get_info(),
            'ram': ram.get_usage(),
            'disk': disk.get_usage(),
            'gpu': gpu.get_usage()
        }

        clear_screen()
        print("\U0001F5A5️  Server Status (Updated Every 1s)")
        print(json.dumps(status, indent=2))
        time.sleep(1)


if __name__ == "__main__":
    main()
