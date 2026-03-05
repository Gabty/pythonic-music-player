import customtkinter as ctk
from tkinter import filedialog
import os
from pathlib import Path

class PlaylistWindow(ctk.CTkToplevel):
    def __init__(self,master, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x200")
        self.title("Playlist ")

        self.grab_set()
        self.lift()
        self.master = master
        self.theme = master.theme
        self.fonts = master.fonts

        self.entry = ctk.CTkEntry(self, width=200)
        self.trial = ctk.CTkButton(self, width=100)

        self.entry.pack()
        self.trial.pack()

    def file_dialog(self):
        pass