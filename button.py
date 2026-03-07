import customtkinter as ctk
from PIL import Image

#global variables
VALID_KEYS = ["fg_color", "text_color", "hover_color", "border_color", "corner_radius", "border_width"]

class PlaylistButton(ctk.CTkButton): # it stores the path of chosen button for easy navigation in Playlist clas

    def __init__(self,master,path,style,*args,**kwargs):
        super().__init__(master, *args, **kwargs)

        self.path = path
        self.state = False # inactive
        self.button_style = {i:j for i,j in style['button'].items() if i in VALID_KEYS}

        self.configure(**self.button_style)
    
    def press(self):
        self.configure()

class ImageButton(ctk.CTkButton):
    def __init__(self, master, image, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.image = self.getImage(*image)
        self.configure(image=self.image, text="")

    @staticmethod
    def getImage(light,dark,size=16):
        return ctk.CTkImage(light_image=Image.open(light),dark_image=Image.open(dark),size=(size,size))

    def setImage(self, img): #
        if img:
            self.configure(image=img)

class MusiclistButton(ImageButton): # it store music name for playing and deleting for Musiclist class
    def __init__(self, master, music,style, image, *args, **kwargs):
        super().__init__(master,image, *args, **kwargs)

        self.music = music
        self.button_style = {i:j for i,j in style['imagebutton'].items() if i in VALID_KEYS}
        self.configure(**self.button_style)
    
    def active(self):
        if not self.active:
            pass