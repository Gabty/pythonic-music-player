import customtkinter as ctk

class MarqueeLabel(ctk.CTkCanvas):
    def __init__(self,master,text,theme,fonts, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        self.fonts = fonts['header']
        self.theme = theme
        mode = 0 if ctk.get_appearance_mode() == 'light' else 1
        print(mode)

        self.configure(width=self.fonts.measure(text),height=self.fonts.metrics('linespace'), bg=self.theme['frame']['fg_color'][mode], highlightthickness=0)
        self.text_id = self.create_text(0,15, anchor='w',text=text, font=self.fonts,fill=self.theme['button']['text_color'][mode])

        self.speed = 1

        self.after(20, self.animate)

    def animate(self):
        self.move(self.text_id, -self.speed, 0)
        x1,y1,x2,y2 = self.bbox(self.text_id)

        if x2<0:
            self.coords(self.text_id, self.winfo_width(), 15)

        self.after(20, self.animate)
