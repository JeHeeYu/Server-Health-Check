import psutil
import time

class CpuMonitor:
    def __init__(self, correction_factor=1.5):
        self.correction_factor = correction_factor

    def get_usage(self):
        samples = []
        for _ in range(10):
            samples.append(psutil.cpu_percent(interval=0.1) / 100.0)
        avg = sum(samples) / len(samples)
        avg = min(max(avg * self.correction_factor, 0), 1)
        return f"{avg * 100:.1f}"

    def get_info(self):
        return {
            'usage': self.get_usage()
        }
