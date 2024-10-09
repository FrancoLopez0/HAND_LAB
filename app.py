import customtkinter as ctk
from view.frames.web_Cam import *

program = "Computer Vision | Robotics Laboratory UTN Fra"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.config()
        self.logo = ctk.CTkFrame(self)
        self.icon = ctk.CTkImage(light_image=Image.open(
            r'assets\images\file.png'), dark_image=Image.open(r'assets\images\file.png'), size=(60, 60))

        self.icon_robotica = ctk.CTkLabel(self.logo, text=" ", image=self.icon)
        self.icon_robotica.grid(row=0, column=0)

        self.robotica = ctk.CTkLabel(self.logo, text="Robotica UTN FRA",
                                     fg_color="transparent", height=60, width=200, font=("Arial", 20))
        self.robotica.grid(row=0, column=1)

        self.logo.pack()

        self.web_Cam = web_Cam(self)
        self.web_Cam.pack(pady=20)
        self.project_Config_ = project_Config(self)
        self.project_Config_.pack()
        # self.project_Config_.bind("<Motion>", self.mouse)

    def mouse(self, e):
        print(e)

    # def Theme_mode(self):
    #     if (self.switch.get()):
    #         self._set_appearance_mode("dark")
    #     else:
    #         self._set_appearance_mode("light")

    def config(self):
        self.title(program)
        self.geometry("1024x700")
        self._set_appearance_mode("dark")

    def on_closing(self):
        web_Cam.on_closing()
        self.destroy()


def mouse(e):
    print(e)


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELTE_WINDOW", app.on_closing)
    # app.bind('<Motion>', mouse)
    app.mainloop()
