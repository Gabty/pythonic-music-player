import customtkinter as ctk
from PIL import Image

#global variables
VALID_KEYS = ["fg_color", "text_color", "hover_color", "border_color", "corner_radius", "border_width"]

class ToggleButton(ctk.CTkButton):
    def __init__(self, master,style,*args, **kwargs):
        self.user_command = kwargs.pop("command", None)
        self.toggle = kwargs.pop('toggle', True) # mostly true
        super().__init__(master,*args, command=self.run, **kwargs)
        # unload theme
        self.b_active = style.get('active_color', None) # get the active color of button
        self.b_style = {k:i for k,i in style.items() if k in VALID_KEYS} # removes unwanted variable
        self.configure(**self.b_style)

        self.active = False
    def run(self):
        if self.user_command:
                self.user_command()
        if not self.toggle:
            return
        self.active = not self.active

        if self.active:
            if self.b_active:
                self.configure(fg_color=self.b_active)
        else:
            self.configure(fg_color=self.b_style['fg_color'])
    
    def set_command(self, command):
        if command:
            self.user_command = command


class PlaylistButton(ToggleButton): # it stores the path of chosen button for easy navigation in Playlist clas
    def __init__(self,master,path,style,*args,**kwargs):
        super().__init__(master,style, *args, **kwargs)
        self.path = path
    
    def press(self):
        self.configure()

class ImageButton(ToggleButton):
    def __init__(self, master,image,style, *args, **kwargs):
        
        kwargs['image'] = self.getImage(*image)
        kwargs['text'] = ""
        super().__init__(master,style, *args, **kwargs)


    @staticmethod
    def getImage(light,dark,size=16):
        return ctk.CTkImage(light_image=Image.open(light),dark_image=Image.open(dark),size=(size,size))

    def setImage(self, img): #
        if img:
            self.configure(image=img)

class MusiclistButton(ImageButton): # it store music name for playing and deleting for Musiclist class
    def __init__(self, master, music,style, image, *args, **kwargs):
        super().__init__(master,image,style, *args, **kwargs)

        self.music = music
    
    def active(self):
        if not self.active:
            pass