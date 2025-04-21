from file import start_file_server
from client.socket_client import SocketClient

if __name__ == '__main__':
    start_file_server()
    SocketClient().run()
