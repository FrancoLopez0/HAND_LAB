import customtkinter as ctk

class slider_Labeled(ctk.CTkFrame):
    def __init__(self, master, label, color, callback, _from_ = 0, _to_ = 100, **kwargs):
        super().__init__(master, **kwargs)

        self._bg_color = color
        self.label = ctk.CTkLabel(self, text=label, bg_color=color,height=20)
        self.label.grid(row=0, column=0)
        self.slider = ctk.CTkSlider(self, width=200,from_=_from_,to=_to_, bg_color=color, command=callback)
        self.slider.grid(row=1, column=0)
    
    def _set_Slider (self, value):
        self.slider.set(value)