import psutil

class RamMonitor:
    def get_usage(self):
        mem = psutil.virtual_memory()
        used_mb = (mem.total - mem.available) / 1024 / 1024
        total_mb = mem.total / 1024 / 1024
        percent = mem.percent
        return {
            'usage': f"{percent:.1f}",
            'used': f"{used_mb:.0f}",
            'total': f"{total_mb:.0f}"
        }
