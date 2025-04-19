from command.command_handler import CommandHandler
from monitors import CpuMonitor, RamMonitor, DiskMonitor, GpuMonitor
from concurrent.futures import ThreadPoolExecutor
from utils import SERVER_URL, SERVER_CODE
import socketio
import time

cpu = CpuMonitor()
ram = RamMonitor()
disk = DiskMonitor()
gpu = GpuMonitor()

def get_status():
    cpu_result = cpu.get_usage()
    gpu_result = gpu.get_usage()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            'ram': executor.submit(ram.get_usage),
            'disk': executor.submit(disk.get_usage),
        }

        result = {'cpu': cpu_result, 'gpu': gpu_result}
        for key, future in futures.items():
            try:
                result[key] = future.result(timeout=1)
            except Exception:
                result[key] = 'N/A'

    return {
        'code': SERVER_CODE,
        'status': result
    }


def start_client():
    while True:
        sio = socketio.Client()

        @sio.event
        def connect():
            print("Connected!")
            sio.emit('init', { 'code': SERVER_CODE })

        @sio.event
        def disconnect():
            print("Disconnected!")

        @sio.on('execute_command')
        def on_execute_command(data):
            target_code = data.get('code')

            if target_code != SERVER_CODE:
                return

            command = data.get('command')
            timestamp = data.get('timestamp')
            print(f"[execute_command] Received command: {command}, timestamp: {timestamp}")

            output = CommandHandler.execute(command)
            print(f"[execute_command] Result:\n{output}")

            print("Jehee emit")
            sio.emit('command_result', {
                'serverId': SERVER_CODE,
                'command': command,
                'result': output
            })



        try:
            sio.connect(SERVER_URL)
        except Exception as e:
            print(f"[connect error] {e}")
            time.sleep(3)
            continue

        try:
            while True:
                if sio.connected:
                    status = get_status()
                    sio.emit('update-status', status)
                    # print("Send status:", status)
                else:
                    print("Lost connection, retrying...")
                    break
        except Exception as e:
            print(f"[loop error] {e}")
        finally:
            try:
                sio.disconnect()
            except:
                pass
            time.sleep(3)  # 재시도 간격
