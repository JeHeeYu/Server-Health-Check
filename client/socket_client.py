import time
import socketio
from concurrent.futures import ThreadPoolExecutor

from command.command_handler import CommandHandler
from monitors import CpuMonitor, RamMonitor, DiskMonitor, GpuMonitor
from utils import SERVER_URL, SERVER_CODE


class SocketClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.cpu = CpuMonitor()
        self.ram = RamMonitor()
        self.disk = DiskMonitor()
        self.gpu = GpuMonitor()
        self._register_events()

    def _register_events(self):
        @self.sio.event
        def connect():
            self.sio.emit('init', {'serverCode': SERVER_CODE})

        @self.sio.event
        def disconnect():
            pass

        @self.sio.on('execute_command')
        def on_execute_command(data):
            if data.get('serverCode') != SERVER_CODE:
                return

            command = data.get('command')
            result = CommandHandler.execute(command)

            self.sio.emit('command_result', {
                'serverCode': SERVER_CODE,
                'command': command,
                'result': result
            })

    def get_status(self):
        cpu_usage = self.cpu.get_usage()
        gpu_usage = self.gpu.get_usage()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                'ram': executor.submit(self.ram.get_usage),
                'disk': executor.submit(self.disk.get_usage),
            }

            status = {
                'cpu': cpu_usage,
                'gpu': gpu_usage
            }

            for key, future in futures.items():
                try:
                    status[key] = future.result(timeout=1)
                except:
                    status[key] = 'N/A'

        return {
            'serverCode': SERVER_CODE,
            'status': status
        }

    def run(self):
        while True:
            try:
                self.sio.connect(SERVER_URL)
            except:
                time.sleep(3)
                continue

            try:
                while self.sio.connected:
                    self.sio.emit('update-status', self.get_status())
                    time.sleep(1)
            except:
                pass
            finally:
                try:
                    self.sio.disconnect()
                except:
                    pass
                time.sleep(3)

def start_socket_client():
    SocketClient().run()