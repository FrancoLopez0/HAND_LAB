import customtkinter as ctk

class slider_Labeled(ctk.CTkFrame):
    def __init__(self, master, label, color, callback, _from_ = 0, _to_ = 100, **kwargs):
        super().__init__(master,fg_color="transparent", **kwargs)

        self._bg_color = color
        self.label = ctk.CTkLabel(self, text=label, bg_color=color,height=20)
        self.label.grid(row=0, column=0)
        self.slider = ctk.CTkSlider(self, width=200,from_=_from_,to=_to_, bg_color=color, command=callback)
        self.slider.grid(row=1, column=0)
    
    def _set_Slider (self, value):
        self.slider.set(value)

class option_Labeled(ctk.CTkFrame):
    def __init__(self, master, color = "transparent", label=None, values=["option 1", "option 2"], callback = None, w = None,**kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        if callback == None:
            return print("Don't have a callback")
        
        self.label = ctk.CTkLabel(self, text=label, bg_color=color,height=20, width=w)
        self.label.grid(row=0, column=0)
        self.select_cam = ctk.CTkOptionMenu(self,  values=values, command=callback, width=w, anchor= "w")
        self.select_cam.grid(row=1, column = 0)