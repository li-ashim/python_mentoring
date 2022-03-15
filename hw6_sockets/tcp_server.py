import os
import socket
from datetime import datetime
from multiprocessing.pool import ThreadPool
from threading import Lock, Thread


def client_handler(client, file):
    """Handle one portion of data from client and save to file."""
    data = client.recv(1024)

    udata = data.decode(encoding='utf-8')
    print(f'Data recieved: {udata}')
    with file_lock:
        print(udata, file=file)


class ServerThread(Thread):
    """Dedicated thread for server."""
    def __init__(self, addr, n_listen=5) -> None:
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(n_listen)

        self._is_running = True  # Running flag

    def run(self):

        with ThreadPool(os.cpu_count()) as pool, open('file.txt', 'a') as file:
            while self._is_running:
                client, _ = self.sock.accept()
                pool.apply_async(client_handler, (client, file))
            # Close the pool and wait for started tasks to complete
            print('Stopping server...')
            pool.close()
            pool.join()
        self.sock.close()

    def stop(self):
        """Softly stops the server."""
        self._is_running = False


if __name__ == '__main__':
    file_lock = Lock()

    server_thread = ServerThread(('localhost', 8888))
    cur_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f'Server started: {cur_time}')
    server_thread.start()

    while True:
        try:
            input()
        except KeyboardInterrupt:
            # Stop server and wait it to complete started tasks
            server_thread.stop()
            server_thread.join()
            break

    cur_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f'Server stopped: {cur_time}')
