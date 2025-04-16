import shutil
import platform

class DiskMonitor:
    def __init__(self, drive="D:"):
        self.drive = drive

    def get_usage(self):
        if platform.system() == 'Windows':
            try:
                usage = shutil.disk_usage(self.drive)
                total = usage.total
                free = usage.free
                used_percent = (1 - free / total) * 100
                free_mb = free / 1024 / 1024
                return {
                    'usage': f"{used_percent:.2f}",
                    'free': f"{free_mb:.0f}"
                }
            except FileNotFoundError:
                return {'usage': 'N/A', 'free': 'N/A'}
        else:
            return {'usage': 'N/A', 'free': 'N/A'}
