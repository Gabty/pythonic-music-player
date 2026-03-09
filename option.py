import customtkinter as ctk
from tkinter import messagebox
import os
import shutil

class OptionWindow(ctk.CTkToplevel):
    def __init__(self,master,data, *args, **kwargs):
        super().__init__(master,*args, **kwargs)

        self.geometry("400x200")
        self.title("Option")
        self.grab_set()
        self.lift()

        self.data = data
        self.master = master
        self.theme = master.theme   
        self.fonts = master.fonts

        self.configure(**self.theme['frame'])

        self.label = ctk.CTkLabel(self, text="Options", font=master.fonts['header'])
        self.renamebtn = ctk.CTkButton(self, text="✎ Rename",width=200, font=self.fonts['header'], **self.theme['button2'], command=self.renameEvent)
        self.deletebtn = ctk.CTkButton(self, text="🗑 Delete",width=200, font=self.fonts['header'], **self.theme['button2'], command=self.deleteEvent)

        self.label.pack(pady=10)
        self.renamebtn.pack(pady=5)
        self.deletebtn.pack(pady=5)

    def renameEvent(self):
        dialog = ctk.CTkInputDialog(text="Input the new name:", title="Rename Playlist", **self.theme['frame'])

        text = dialog.get_input()

        if text is None:
            return

        if not text.strip():
            messagebox.showerror("Value Error", "Empty Field")

        self.data["title"] = text
        self.master.saveJSON(self.data)
        self.master.refresh()
    
    def deleteEvent(self):
        main = self.master.master # main class
        if os.path.exists(self.master.path):
            shutil.rmtree(self.master.path)
        first = main.playListFrame.getFirstPlayList()
        main.setPlaylist(first)
        self.destroy()
        main.after(40, main.playListFrame.reload_listframe)
        