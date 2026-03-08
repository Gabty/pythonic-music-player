import customtkinter as ctk

class Label(ctk.CTkLabel):
    def __init__(self,master, text,font, *args, **kwargs):
        super().__init__(master,text=text,font=font, *args, **kwargs)
    
    def setText(self, text):
        self.configure(text=text)

class MarqueeLabel(ctk.CTkCanvas):
    def __init__(self,master,text,theme,fonts, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        self.fonts = fonts['header']
        self.theme = theme
        self.mode = 0 if ctk.get_appearance_mode() == 'light' else 1

        self.canvas_width = 360
        self.text_width = self.fonts.measure(text)
        # set 
        self.configure(width=self.canvas_width,height=self.fonts.metrics('linespace'), bg=self.theme['fg_color'][self.mode], highlightthickness=0)
        self.text_id = self.create_text(0,self.fonts.metrics('linespace')//2, anchor='w',text=text, font=self.fonts,fill=self.theme['text_color'][self.mode])
        # speed
        self.speed = 0.96
        # move
        self.after_id = self.after(20, self.animate)

    def animate(self):
        self.move(self.text_id, self.speed, 0)
        x1,y1,x2,y2 = self.bbox(self.text_id)

        if x1>self.canvas_width:
            self.coords(self.text_id, -(x2-x1), self.fonts.metrics('linespace')//2)

        self.after_id = self.after(20, self.animate)
    
    def setText(self,text):
        if hasattr(self, 'after_id'):
            self.after_cancel(self.after_id)

        self.delete('all')
        self.configure(width=self.canvas_width,height=self.fonts.metrics('linespace'), bg=self.theme['fg_color'][self.mode], highlightthickness=0)
        self.text_id = self.create_text(0,self.fonts.metrics('linespace')//2, anchor='w',text=text, font=self.fonts,fill=self.theme['text_color'][self.mode])

        self.after_id = self.after(20, self.animate)