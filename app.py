import customtkinter as ctk
from view.frames.web_Cam import *

program = "Computer Vision | Robotics Laboratory UTN Fra"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config()

        self.web_Cam = web_Cam(self)
        self.web_Cam.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.web_Cam_config = web_Cam_config(self)
        self.web_Cam_config.grid(row=0, column=1)
    
    def optionmenu_callback(self, choice):
        print(choice)
    
    def config(self):
        self.title(program)

        self.geometry("1024x600")
        self._set_appearance_mode("dark")

    def slider_event(self):
        print("Slider")

    def on_closing(self):
        web_Cam.on_closing()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELTE_WINDOW", app.on_closing)
    app.mainloop()

        