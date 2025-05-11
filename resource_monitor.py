import psutil
import shutil
import time

try:
    import GPUtil
    gpu_available = True
except ImportError:
    gpu_available = False

class ResourceMonitor:
    def __init__(self, disk_drive="/home", cpu_correction_factor=1.5):
        self.disk_drive = disk_drive
        self.cpu_correction_factor = cpu_correction_factor

    def get_cpu_usage(self):
        samples = [psutil.cpu_percent(interval=0.1) / 100.0 for _ in range(10)]
        avg = sum(samples) / len(samples)
        avg = min(max(avg * self.cpu_correction_factor, 0), 1)
        return f"{avg * 100:.1f}"

    def get_ram_usage(self):
        mem = psutil.virtual_memory()
        used_mb = (mem.total - mem.available) / 1024 / 1024
        total_mb = mem.total / 1024 / 1024
        return {
            'usage': f"{mem.percent:.1f}",
            'used': f"{used_mb:.0f}",
            'total': f"{total_mb:.0f}"
        }

    def get_disk_usage(self):
        try:
            usage = shutil.disk_usage(self.disk_drive)
            total = usage.total
            free = usage.free
            used_percent = (1 - free / total) * 100
            free_mb = free / 1024 / 1024
            return {
                'usage': f"{used_percent:.1f}",
                'free': f"{free_mb:.0f}"
            }
        except FileNotFoundError:
            return {'usage': 'N/A', 'free': 'N/A'}

    def get_gpu_usage(self):
        if not gpu_available:
            return {'usage': 'N/A'}
        try:
            gpus = GPUtil.getGPUs()
            return {'usage': f"{gpus[0].load * 100:.1f}"} if gpus else {'usage': 'N/A'}
        except:
            return {'usage': 'N/A'}

    def get_network_usage(self, interval=1, link_speed_mbps=1000):
        try:
            net1 = psutil.net_io_counters()
            time.sleep(interval)
            net2 = psutil.net_io_counters()
            total_bytes = (net2.bytes_sent + net2.bytes_recv) - (net1.bytes_sent + net1.bytes_recv)
            speed_bps = (total_bytes * 8) / interval
            usage_percent = (speed_bps / (link_speed_mbps * 1_000_000)) * 100
            return {'usage': f"{usage_percent:.1f}"}
        except:
            return {'usage': 'N/A'}

    def get_all(self):
        return {
            'cpu': self.get_cpu_usage(),
            'ram': self.get_ram_usage(),
            'disk': self.get_disk_usage(),
            'gpu': self.get_gpu_usage(),
            'network': self.get_network_usage()
        }
