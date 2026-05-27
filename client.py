import socket
import threading
from colorama import Fore, Back, Style, init

init(autoreset=True)

IP = "127.0.0.1"
PORT = 12345
ADDR = (IP,PORT)

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

name = input("CHOOSE A USERNAME :")
name = name.strip()
 
def receive():
    while True:
        try:
            msg = client_socket.recv(4096).decode('utf-8')
            if msg == 'NAME':
                client_socket.send(name.encode('utf-8'))
            else:
                print(msg)
        except:
            print("An error occurred !")
            client_socket.close()
            break

def write():
    while True:
        msg = input('')
        if msg.isspace():
            print(f'{Colors.RED}Texts can not be empty {Colors.RESET}')
            continue
        msg = msg.strip()
        client_socket.send(msg.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
            