from view.frames.my_Frames import *
from controllers.hand_Tracking_controller import *
from PIL import Image, ImageTk

cam = hand_Tracking_controller(1)

class web_Cam_config(ctk.CTkFrame):
    def __init__(self, master, color = "transparent", **kwargs):
        super().__init__(master, **kwargs)

        self._bg_color = color

        self.distance = slider_Labeled(self, "Distance", color="transparent", callback=self.distance_Slider)
        self.distance._set_Slider(cam.get_distance())
        self.distance.grid(row=0, column=0)

        self.square = slider_Labeled(self, "Square", color="transparent", callback=self.square_Slider)
        self.distance._set_Slider(cam.get_Square())
        self.square.grid(row=1, column=0)
    
    def square_Slider(self, value):
        cam.change_Square(value)
    
    def distance_Slider(self, value):
        cam.change_Distance(value)

class web_Cam(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.video_frame=ctk.CTkFrame(self, width=800, height=600)

        self.video_frame.pack()

        self.label = ctk.CTkLabel(self.video_frame)
        self.label.pack()
        self.update_frame()

        self.config = web_Cam_config(self,cam_config=cam)

    def update_frame(self):
        
        ret, cam.frame_0 = cam.cap.read()
        
        if ret:
            cam._program_()
            img = Image.fromarray(cam.frame_0)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.configure(image=imgtk)

        self.after(10, self.update_frame)
    
    def on_closing(self):
        cam.cap.release()

