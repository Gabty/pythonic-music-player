import customtkinter as ctk

#global variables
VALID_KEYS = ["fg_color", "text_color", "hover_color", "border_color", "corner_radius", "border_width"]

class PlaylistButton(ctk.CTkButton):

    def __init__(self,master,path,style,*args,**kwargs):
        super().__init__(master, *args, **kwargs)

        self.path = path
        self.button_style = {i:j for i,j in style['button'].items() if i in VALID_KEYS}

        self.configure(**self.button_style)


class MusiclistButton(ctk.CTkButton):
    def __init__(self, master, music,style, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.music = music
        self.button_style = {i:j for i,j in style['button'].items() if i in VALID_KEYS}
