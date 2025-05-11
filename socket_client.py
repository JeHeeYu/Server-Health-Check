from command_handler import CommandHandler
from resource_monitor import *
from concurrent.futures import ThreadPoolExecutor
from config import *
import socketio
import time
import platform

if platform.system() == 'Windows':
    disk_path = "D:" 
else:
    disk_path = "/home"

monitor = ResourceMonitor(disk_drive=disk_path)

def get_status():
    result = monitor.get_all()
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
            sio.emit('init', { 'serverCode': SERVER_CODE })

        @sio.event
        def disconnect():
            print("Disconnected!")

        @sio.on('execute_command')
        def on_execute_command(data):
            target_code = data.get('serverCode')

            if target_code != SERVER_CODE:
                return

            command = data.get('command')
            timestamp = data.get('timestamp')
            print(f"[execute_command] Received command: {command}, timestamp: {timestamp}")

            output = CommandHandler.execute(command)
            print(f"[execute_command] Result:\n{output}")

            sio.emit('command_result', {
                'serverCode': SERVER_CODE,
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
            time.sleep(3)
