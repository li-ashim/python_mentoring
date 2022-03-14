import random
import socket
from datetime import datetime
from time import sleep


def main_loop():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 8888))
            data = (datetime.now().isoformat(sep=' ', timespec='seconds')
                    + '\t' + str(random.random())).encode('utf-8')
            client_socket.send(data)
        except ConnectionRefusedError:
            print('Connection failed.')
            break
        except KeyboardInterrupt:
            break
        finally:
            client_socket.close()

        sleep(60)


if __name__ == '__main__':
    cur_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f'Client started {cur_time}')
    main_loop()
    cur_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f'Client stopped {cur_time}')
