import socketio
import time
from monitors import CpuMonitor, RamMonitor, DiskMonitor, GpuMonitor
from utils import SERVER_URL, SERVER_CODE

sio = socketio.Client()
cpu = CpuMonitor()
ram = RamMonitor()
disk = DiskMonitor()
gpu = GpuMonitor()

@sio.event
def connect():
    print('server connected')

@sio.event
def disconnect():
    print('server disconnected')

def get_status():
    return {
        'code': SERVER_CODE,
        'status': {
            'cpu': cpu.get_usage(),
            'ram': ram.get_usage(),
            'disk': disk.get_usage(),
            'gpu': gpu.get_usage()
        }
    }

def start_client():
    sio.connect(SERVER_URL)

    try:
        while True:
            status = get_status()
            sio.emit('update-status', status)
            print("Send status : ", status)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Close")
    finally:
        sio.disconnect()
