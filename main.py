import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import json
from pathlib import Path
import os
#import pygame.mixer as mx

from option import OptionWindow
from buttons import PlaylistButton

# global keys
DOCUMENTS = Path.home() / "Documents"
FOLDER = "Music Player"
PATH = DOCUMENTS/FOLDER

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Window Size
        self.geometry("1280x780")
        self.title("Audio Player")
        # Style
        # Unload the file
        with open('style.json', 'r+') as f:
            style = json.load(f)
        
        #Unpack the JSON "style"
        theme = style["style"]
        fonts = {i:ctk.CTkFont(size=style["font"][i]["size"], weight=style["font"][i]["weigth"]) for i in style["font"]}

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize= 80)

        # Frames
        # Frame that play, stop, backward, or forward a music
        self.playerFrame = Player(self, theme, fonts, fg_color=theme["frame"]["fg_color"])
        self.playerFrame.grid(row=1, columnspan=2, sticky='nsew',padx=1,pady=1)
        # local playlist
        self.playListFrame = Playlist(self,theme,fonts, fg_color="transparent")
        self.playListFrame.grid(row=0, column=0, sticky='nsew',padx=1,pady=1)
        # list of audio in a playlist
        self.musicListFrame = Musiclist(self,theme, fonts, fg_color="transparent")
        self.musicListFrame.grid(row=0, column=1, sticky='nsew',padx=1,pady=1)
    
    def setPlaylist(self, path): # called by Playlistframe
        self.musicListFrame.load_music(path) # runs musiclistframe function

class Player(ctk.CTkFrame):
    def __init__(self, master,theme, fonts, **kwargs):
        super().__init__(master,**kwargs)

        self.label = ctk.CTkLabel(self, text="Hello", font=fonts["header"])
        self.label.pack()

class Playlist(ctk.CTkFrame):
    def __init__(self, master,theme, fonts, **kwargs):
        super().__init__(master, **kwargs)
        # top level
        self.toplevel = None
        # font
        self.fonts = fonts
        self.theme = theme
        # image
        self.plus = getImage('img/plus-symbol-button-b.png', "img/plus-symbol-button-w.png", 16)
        # grid configuration
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=0, minsize=80)
        self.grid_rowconfigure(1,weight=1)
        # frames
        self.header = ctk.CTkFrame(self, height=80, fg_color=self.theme["frame"]["fg_color"])
        self.list = ctk.CTkScrollableFrame(self,fg_color=self.theme["frame"]["fg_color"])
        # instance
        self.header.grid(row=0,column=0, sticky='nsew',padx=1,pady=1)
        self.list.grid(row=1,column=0, sticky='nsew',padx=1,pady=1)

        #Header
        self.header.grid_rowconfigure(0,weight=1)
        self.header.grid_columnconfigure(0,weight=1)
        self.header.grid_columnconfigure(1,weight=0)
        self.header.grid_columnconfigure(2,weight=1)

        self.header_title = ctk.CTkLabel(self.header, text="♫ Playlist ♫", font=self.fonts["header"])
        self.header_button = ctk.CTkButton(self.header, image=self.plus,text="",width=32,height=32,font=self.fonts["main"], command=self.create_playlist)

        #packing
        self.header_title.grid(row=0,column=1)
        self.header_button.grid(row=0,column=2,sticky='se',padx=5,pady=5)
        self.start()
        self.active=None

    def start(self):
        folders = Path(PATH).iterdir()
        for path in folders:
            button = PlaylistButton(self.list, path=str(path),text=path.name,style=self.theme, font=self.fonts["main"],anchor='w',height=60,)
            button.configure(command= lambda b=button: self.load_musiclist(b))

            button.pack(fill='x', expand=True, padx=[1,1], pady=[1,1])
    
    def flush_listframe(self): # only to be called when creating playlist
        for widget in self.list.winfo_children():
            widget.destroy()
    
    def create_playlist(self):
        dialog = ctk.CTkInputDialog(text="Name of playlist ♫", title="Test")

        foldername = dialog.get_input()

        if not foldername:
            messagebox.showerror("Value Error", "Empty Field") # if the foldername is empty
            return

        newpath = PATH/foldername

        if os.path.exists(newpath):
            messagebox.showerror("File Error", "Folder Already Exists") # if the path already exists
            return
        
        os.mkdir(newpath) # create folder for playlist
        contents = {"title": foldername, "sings": []} # for future purposes
        with open(newpath/"list.json", 'w') as f:
            json.dump(contents,f)
        
        self.reload_listframe()
    
    def reload_listframe(self):
        self.flush_listframe()
        self.start()

    def load_musiclist(self, button):
        if self.active: # revert the color back to normal state
            self.active.configure(fg_color=self.theme["button"]['fg_color'])
        elif self.active == button: # check if active and b is same
            return # return if b is same as active
        self.active = button # change the active to new button
        self.active.configure(fg_color=self.theme["button"]['active_color']) # change the color of new button to active color
        self.master.setPlaylist(self.active.path) # load this from main then passed to MusiclistFrame

class Musiclist(ctk.CTkFrame):
    def __init__(self, master,theme, fonts, **kwargs):
        super().__init__(master, **kwargs)
        # top level
        self.toplevel = None
        # initialize font/theme
        self.theme = theme
        self.fonts = fonts
        # instanciate image
        self.three_dots = getImage('img/dots.png', 'img/dots-w.png', 24)
        # grid configuration
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=0, minsize=80)
        self.grid_rowconfigure(1,weight=1)
        # Frame Instance
        self.header = ctk.CTkFrame(self, height=80, **self.theme["frame"])
        self.list = ctk.CTkScrollableFrame(self,**self.theme["frame"])
        # Grid
        self.header.grid(row=0,column=0,sticky='nsew',pady=1,padx=1)
        self.list.grid(row=1,column=0,sticky='nsew',pady=1,padx=1)
        # header grid config
        self.header.grid_rowconfigure(0,weight=1)
        self.header.grid_columnconfigure(0,weight=0)
        self.header.grid_columnconfigure(1,weight=1)
        self.header.grid_columnconfigure(2,weight=1)
        # Header Widgets
        self.header_title = ctk.CTkLabel(self.header, text="", font=self.fonts["header"])
        self.header_menu = ctk.CTkButton(self.header,text="⋮",width=32,height=32,font=self.fonts["main"], command=self.option_toplevel)
        # Grid Widget
        self.header_title.grid(row=0,column=0,padx=5)
        self.header_menu.grid(row=0,column=2,sticky='e',padx=5,pady=5)

    def load_music(self,path):# called from main class
        print(path)
    def option_toplevel(self):
        if self.toplevel == None or not self.toplevel.winfo_exists():
            self.toplevel = OptionWindow(self)
        else:
            self.toplevel.focus()
        

def getImage(light,dark,size=16):
    return ctk.CTkImage(light_image=Image.open(light),dark_image=Image.open(dark),size=(size,size))

if __name__ == "__main__":
    if (not os.path.exists(PATH)):
        print("Hello")
        os.mkdir(PATH)

    ctk.set_appearance_mode('dark')
    app = MainApp()
    app.mainloop()