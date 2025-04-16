import subprocess
import time

class GpuMonitor:
    def __init__(self, correction_factor=1.5):
        self.correction_factor = correction_factor

    def get_usage(self):
        usages = []
        mem_used = mem_total = None

        for _ in range(10):
            try:
                output = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total', '--format=csv,nounits,noheader'],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()

                gpu_util, mu, mt = output.split(', ')
                usages.append(int(gpu_util))
                mem_used = int(mu)
                mem_total = int(mt)

            except:
                continue

            time.sleep(0.1)

        if not usages or mem_used is None or mem_total is None:
            return {
                'usage': 'N/A',
                'used': 'N/A',
                'total': 'N/A',
                'memory': 'N/A'
            }

        avg_gpu = sum(usages) / len(usages)
        avg_gpu = min(max(avg_gpu * self.correction_factor, 0), 100)
        mem_percent = (mem_used / mem_total) * 100

        return {
            'usage': f"{avg_gpu:.0f}",
            'used': f"{mem_used}",
            'total': f"{mem_total}",
            'memory': f"{mem_percent:.2f}"
        }
