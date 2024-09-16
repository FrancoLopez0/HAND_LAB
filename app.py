import customtkinter as ctk
from view.frames.web_Cam import *

program = "Computer Vision | Robotics Laboratory UTN Fra"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config()

        self.web_Cam = web_Cam(self)
        self.web_Cam.pack()
        #self.web_Cam.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.web_Cam.bind("<Motion>", self.mouse)
        self.project_Config_ = project_Config(self)
        #self.project_Config_.place(x=0, y=485)
        self.project_Config_.pack()
        self.project_Config_.bind("<Motion>", self.mouse)

        #self.ligth = ctk.StringVar("off")
        self.switch = ctk.CTkSwitch(self, text="Mode", command=self.Theme_mode)
        self.switch.pack()
    
    def mouse(self, e):
        print(e)

    def Theme_mode(self):
        if(self.switch.get()):
            self._set_appearance_mode("dark")
        else:
            self._set_appearance_mode("light")

    def config(self):
        self.title(program)

        self.geometry("1024x600")
        self._set_appearance_mode("light")

    def on_closing(self):
        web_Cam.on_closing()
        self.destroy()


def mouse(e):
    print(e)
    
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELTE_WINDOW", app.on_closing)
    app.bind('<Motion>', mouse)
    app.mainloop()

        