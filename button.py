import customtkinter as ctk
from PIL import Image

#global variables
VALID_KEYS = ["fg_color", "text_color", "hover_color", "border_color", "corner_radius", "border_width"]

class Button(ctk.CTkButton):
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
    
    def set_command(self, command): # set new command
        if command:
            self.user_command = command
    
    @staticmethod
    def getImage(light,dark,size=16):
        return ctk.CTkImage(light_image=Image.open(light),dark_image=Image.open(dark),size=(size,size))

    def setImage(self, img): #
        if img:
            self.configure(image=img)


class PlaylistButton(Button): # Inherits Button and store path
    def __init__(self,master,path,style,*args,**kwargs):
        super().__init__(master,style, *args, **kwargs)
        self.path = path
    
    def press(self):
        self.configure()

class ImageButton(Button): # Inherit Button
    def __init__(self, master,image,style, *args, **kwargs):
        
        kwargs['image'] = self.getImage(*image)
        kwargs['text'] = ""
        super().__init__(master,style, *args, **kwargs)

class ToggleImageButton(Button):
    def __init__(self, master, images, style,commands, *args, **kwargs):
        self.commands = commands
        self.width = kwargs.get('width')
        self.pre_images = [self.getImage(*i, self.width) for i in images]
        kwargs['image'] = self.pre_images[0]
        kwargs['text'] = ""
        super().__init__(master, style, *args, **kwargs)
        self.is_pause = self.active
    def run(self):
        self.is_pause = not self.is_pause
        if not self.is_pause:
            self.commands[0]() # first command
        else:
            self.commands[1]() # second command
        self.setImage(self.pre_images[self.is_pause])


class MusiclistButton(ImageButton): # Inherits ImageButton and store music
    def __init__(self, master, music,style, image, *args, **kwargs):
        super().__init__(master,image,style, *args, **kwargs)

        self.music = music
    
    def active(self):
        if not self.active:
            pass