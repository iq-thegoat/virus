import socket
import threading
from colorama import Fore
import colorama

colorama.init()

green,reset  =  Fore.GREEN,Fore.RESET 
PORT         =  5050
SERVER       =  socket.gethostbyname(socket.gethostname())
ADDR         =  (SERVER,PORT)
server       =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_clinet(conn,addr):
    print(f"{green}[NEW CONNECTION] {Fore.RED}{addr}{Fore.RESET} Fell in the trap")
    connected = True
    while connected:
        recvd = conn.recv()

def get_active_connections():
    return f"{green}[CONNECTED VICTIMS] {threading.active_count() -1}"

def start():
    server.listen()
    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target=handle_clinet,args=(conn,addr))
        thread.start()
        print(get_active_connections())



print("[STARTING] Starting Server")
start()