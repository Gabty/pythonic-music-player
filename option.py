import customtkinter as ctk
import json

class OptionWindow(ctk.CTkToplevel):
    def __init__(self,master, *args, **kwargs):
        super().__init__(master,*args, **kwargs)

        self.geometry("400x200")
        self.title("Option")
        self.grab_set()
        self.lift()

        self.theme = master.theme
        self.fonts = master.fonts

        self.configure(**self.theme['frame'])

        self.label = ctk.CTkLabel(self, text="Options", font=master.fonts['header'])
        self.renamebtn = ctk.CTkButton(self, text="✎ Rename",width=200, font=self.fonts['header'], **self.theme['button2'], command=self.renameEvent)
        self.deletebtn = ctk.CTkButton(self, text="🗑 Delete",width=200, font=self.fonts['header'], **self.theme['button2'])

        self.label.pack(pady=10)
        self.renamebtn.pack(pady=5)
        self.deletebtn.pack(pady=5)

    def renameEvent(self):
        dialog = ctk.CTkInputDialog(text="Input the new name:", title="Rename Playlist", **self.theme['frame'])