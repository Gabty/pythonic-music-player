import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path
import shutil
import os
#import pygame.mixer as mx

from option import OptionWindow
from button import PlaylistButton, MusiclistButton, ImageButton
from label import Label, MarqueeLabel

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
        # Unload the JSON FILES

        with open('config/style.json', 'r') as fp: # 
            style = json.load(fp)

        with open('config/images.json', 'r') as fp: # get dict of icons
            self.images = json.load(fp)
        
        #Unpack the style to theme and fonts
        self.theme = style["style"]
        self.fonts = {i:ctk.CTkFont(size=style["font"][i]["size"], weight=style["font"][i]["weigth"]) for i in style["font"]}

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize= 80)

        # Frames
        # Frame that play, stop, backward, or forward a music
        self.playerFrame = Player(self, theme=self.theme, fonts=self.fonts,images=self.images,  fg_color=self.theme["frame"]["fg_color"])
        self.playerFrame.grid(row=1, columnspan=2, sticky='nsew',padx=1,pady=1)
        # local playlist
        self.playListFrame = Playlist(self,self.theme,self.fonts,images=self.images, fg_color="transparent")
        self.playListFrame.grid(row=0, column=0, sticky='nsew',padx=1,pady=1)
        # list of audio in a playlist
        self.musicListFrame = Musiclist(self,self.theme, self.fonts,images=self.images, fg_color="transparent")
        self.musicListFrame.grid(row=0, column=1, sticky='nsew',padx=1,pady=1)

        self.setPlaylist(self.playListFrame.getFirstPlayList())
    
    def setPlaylist(self, path): # called by Playlistframe
        self.musicListFrame.loadPlaylist(path) # runs musiclistframe function

class Player(ctk.CTkFrame):
    def __init__(self, master,theme, fonts,images, **kwargs):
        super().__init__(master,**kwargs)
        self.theme = theme
        self.fonts = fonts
        self.images = images
        self.label = MarqueeLabel(self, "HELLLOOO",self.theme, self.fonts)
        self.label.pack()

class Playlist(ctk.CTkFrame):
    def __init__(self, master,theme, fonts,images, **kwargs):
        super().__init__(master, **kwargs)
        # top level
        self.toplevel = None
        # font
        self.fonts = fonts
        self.theme = theme
        # image
        self.images = images
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

        self.header_title = Label(self.header, text="♫ Playlist ♫", font=self.fonts["header"])
        self.header_button = ImageButton(self.header, image=(*self.images['plus'],16),style=self.theme['button'],width=32,height=32,font=self.fonts["main"], command=self.createPlaylist,toggle=False)

        #packing
        self.header_title.grid(row=0,column=1)
        self.header_button.grid(row=0,column=2,sticky='se',padx=5,pady=5)
        self.start()
        self.active=None

    def start(self):
        folders = Path(PATH).iterdir()
        for path in folders:
            button = PlaylistButton(self.list, path=path,text=path.name,style=self.theme['button'], font=self.fonts["main"],anchor='w',height=60)
            button.configure(command= lambda b=button: self.loadMusiclist(b))

            button.pack(fill='x', expand=True, padx=[1,1], pady=[1,1])
    
    def flushListframe(self): # only to be called when reloading playlist after adding
        for widget in self.list.winfo_children():
            widget.destroy()
        self.active = None
    
    def createPlaylist(self):
        dialog = ctk.CTkInputDialog(text="Name of playlist ♫", title="Test")

        foldername = dialog.get_input()

        if foldername is None: # Cancelled
            return

        if not foldername.strip(): # String Input is space or empty but pressed ok
            messagebox.showerror("Value Error", "Empty Field") # if the foldername is empty
            return


        newpath = PATH/foldername

        if os.path.exists(newpath):
            messagebox.showerror("File Error", "Folder Already Exists") # if the path already exists
            return
        
        os.mkdir(newpath) # create folder for playlist
        contents = {"title": foldername, "songs": []} # for future purposes
        with open(newpath/"list.json", 'w') as f:
            json.dump(contents,f)
        
        self.reload_listframe()

    def reload_listframe(self):
        self.flushListframe()
        self.start()

    def loadMusiclist(self, button):
        if self.active and self.active.winfo_exists(): # revert the color back to normal state
            self.active.configure(fg_color=self.theme["button"]['fg_color'])
        if self.active == button: # check if active and b is same then  return if same
            return 
        self.active = button # change the active to new button
        self.active.configure(fg_color=self.theme["button"]['active_color']) # change the color of new button to active color
        self.master.setPlaylist(self.active.path) # load this from main then passed to MusiclistFrame

    def getFirstPlayList(self):
        folder = next(Path(PATH).iterdir(),None)
        return folder if folder else None

class Musiclist(ctk.CTkFrame):
    def __init__(self, master,theme, fonts, images, **kwargs):
        super().__init__(master, **kwargs)
        # top level
        self.toplevel = None
        # initialize font/theme/images
        self.theme = theme
        self.fonts = fonts
        self.images = images
        # initialize variables
        self.path = None
        self.listJSON = None
        # init images
        """self.dots_img = getImage('img/dots.png', 'img/dots-w.png', 16)
        self.plus_img = getImage('img/plus.png', 'img/plus-w.png', 16)

        self.play = getImage('img/play_arrow.png', 'img/play_arrow-w.png', 24)
        self.trash = getImage('img/trash-bin.png', 'img/trash-bin-w.png', 24)"""
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
        self.header_title = Label(self.header, text="",width=200, font=self.fonts["header"],anchor="w")
        # Header container
        self.container_button = ctk.CTkFrame(self.header)#
        self.header_adder = ImageButton(self.container_button,image=(*self.images['plus'], 16),style=self.theme['button'], width=32, height=32, command=self.addMusic,toggle=False)
        self.header_menu = ImageButton(self.container_button,image=(*self.images['dot'], 16),style=self.theme['button'],width=32,height=32, command=self.optionMenu,toggle=False)
        # Grid Widget
        self.header_title.grid(row=0,column=0,padx=40)
        self.container_button.grid(row=0,column=2,sticky='e',padx=5,pady=5)
        self.header_adder.pack(side='left',padx=5)
        self.header_menu.pack(side='left',padx=5)
    def optionMenu(self):
        if self.toplevel == None or not self.toplevel.winfo_exists():
            self.toplevel = OptionWindow(self)
        else:
            self.toplevel.focus()

    def loadPlaylist(self,path):# called from main class
        self.flushListframe()
        self.path = path
        if not path:
            return
        with open(path/"list.json", "r+", encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.header_title.setText(self.data['title'])

        self.start() # 

    def start(self): # loads the musics
        for song in self.data['songs']:
            container = ctk.CTkFrame(self.list, **self.theme['frame2'], height=60) # container
            container.pack_propagate(False)
            # widget of container
            startbutton = MusiclistButton(container, image=(*self.images['play_arrow'], 24),style=self.theme['imagebutton'],width=26,height=26, music=song, toggle=False) 
            label = ctk.CTkLabel(container, text=ellipsis(song,70), font=self.fonts['main'],anchor='w')
            deletebutton = MusiclistButton(container, image=(*self.images['trash'], 24),style=self.theme['imagebutton'],width=26,height=26, music=song, toggle=False)
            deletebutton.set_command(command=lambda b=deletebutton: self.removeMusic(b))

            startbutton.pack(side='left',padx=[20,10])
            label.pack(side='left')
            deletebutton.pack(side='right',padx=[5,20])
            container.pack(side='top',fill='x',pady=1)

    
    def refresh(self): # refresh the framelist
        self.flushListframe() 
        self.loadPlaylist(self.path)
    
    def addMusic(self):
        file = ctk.filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.ogg")]) # accepts .mp3 and .ogg

        if not file: 
            return

        source = Path(file)
        if source.name in self.data['songs']: # prevent duplicate name file
            return
        destination = self.path / source.name

        self.data["songs"].append(source.name)

        with open(self.path/"list.json", "w", encoding="utf-8") as fp:
            json.dump(self.data, fp, indent=4, ensure_ascii=False)

        shutil.copy2(source, destination) # make a copy of music

        self.refresh()


    def removeMusic(self, button):
        file = self.path / button.music
        if file.exists(): # failsafe deletion
            file.unlink()

        self.data['songs'].remove(button.music) # remove the chosen music in data
        with open(self.path/"list.json", "w", encoding="utf-8") as fp:
            json.dump(self.data, fp, indent=4, ensure_ascii=False)

        self.refresh()

    def flushListframe(self):
        for widget in self.list.winfo_children():
            widget.destroy()
        self.data = None

def ellipsis(text, max_length=20):
    return text if len(text) <= max_length else text[:max_length-3] + "..."

if __name__ == "__main__":
    if (not os.path.exists(PATH)):
        os.mkdir(PATH)

    ctk.set_appearance_mode('dark')
    app = MainApp()
    app.mainloop()