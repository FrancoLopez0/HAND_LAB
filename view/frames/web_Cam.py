from view.frames.my_Frames import *
from controllers.hand_Tracking_controller import *
from controllers.video_Cam_controller import *
from PIL import Image, ImageTk
from controllers import wifi

# Select cam object
wifi_name = 'ESP32-Access-Point'
wifi_manager = wifi.WifiManager()

esp32_object = Esp32Cam() if wifi_manager.is_connected(wifi_name) else None

video_capture = cv2.VideoCapture(0)
capture_object = esp32_object if esp32_object else video_capture

cam = hand_Tracking_controller(1, cap=video_capture)

class web_Cam_config(ctk.CTkFrame):
    def __init__(self, master, color = "transparent", **kwargs):
        super().__init__(master,width=50, fg_color="transparent", **kwargs)

        self.video_ = video()
        cams = self.video_.list_availables_cam()
        if esp32_object:
            cams.append("esp_32")
            print('Cam detected:', esp32_object)

        self.choice_Cam = option_Labeled(self, label="Choice Cam", callback=self.choice_Cam_callback, w = 100, values=cams)
        self.choice_Cam.grid(row = 0, column = 0, padx=20)

        self.choice_Com = option_Labeled(self, label="COM", callback=self.choice_Com_callback, w = 100)
        self.choice_Com.grid(row = 1, column = 0, padx=20)
    
    def choice_Cam_callback(self, choice):
        if choice == 'esp_32':
            cam.cap = esp32_object
        else:
            cam.cap = video_capture
    
    def choice_Com_callback(self, choice):
        print(choice)

class hands_Parameters_config(ctk.CTkFrame):
    def __init__(self, master, color = "transparent", **kwargs):
        super().__init__(master,fg_color="transparent", **kwargs)

        self._bg_color = color
        
        self.time_movement_label = slider_Labeled(self, "Sample Time", color="transparent", callback=self.set_time_slider,
        _from_ = 50,
        _to_ = 150)
        self.time_movement_label._set_Slider(100)
        self.time_movement_label.grid(row=3, column=0)

        self.distance = slider_Labeled(self, "Distance", color="transparent", callback=self.distance_Slider)
        self.distance._set_Slider(cam.get_distance())
        self.distance.grid(row=1, column=0)

        self.square = slider_Labeled(self, "Square", color="transparent", callback=self.square_Slider)
        self.distance._set_Slider(cam.get_Square())
        self.square.grid(row=2, column=0)
    
    def choice_Com_callback(self, choice):
        print(choice)

    def choice_Cam_callback(self, choice):
        print(choice)
    
    def set_time_slider(self, value):
        try:
            cam.change_time(value)
        except AttributeError:
            pass

    def square_Slider(self, value):
        cam.change_Square(value)
    
    def distance_Slider(self, value):
        cam.change_Distance(value)

class checkboxes(ctk.CTkFrame):
    def __init__(self, master, webCam:hand_Tracking_controller = None, **kwargs):
        super().__init__(master,fg_color="transparent", **kwargs)

        self.web_Cam = webCam

        self.var_Tracking = ctk.BooleanVar(value=True)
        self.tracking_On = ctk.CTkCheckBox(self, text="Tracking", hover=True, command=self.tracking, variable=self.var_Tracking, onvalue=True, offvalue=False)
        self.tracking_On.grid(row=0, column=0, padx=10, pady=10)

        self.var_Show_grid = ctk.BooleanVar(value=False)
        self.show_Grid = ctk.CTkCheckBox(self, text="Show Grid", hover=False, command=self.show_grid, variable=self.var_Show_grid, onvalue=True, offvalue=False)
        self.show_Grid.grid(row=1, column=0, padx=10, pady=10)

        # self.ai_View = ctk.CTkCheckBox(self, text="Ai View", hover=False)
        # self.ai_View.grid(row=0, column=1, padx=10, pady=10)

        # self.filters = ctk.CTkCheckBox(self, text="Filters", hover=False)
        # self.filters.grid(row=1, column=1, padx=10, pady=10)
    
    def show_grid(self):
        cam.show_grid_command(self.var_Show_grid.get())
    
    def tracking(self):
        cam.set_Tracking(self.var_Tracking.get())



class project_Config(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,fg_color="transparent", **kwargs)
        self.web_Cam_config = web_Cam_config(self)
        self.web_Cam_config.grid(row=0, column = 0)

        self.conditionals = checkboxes(self)
        self.conditionals.grid(row=0, column=1)

        self.hands_Params = hands_Parameters_config(self)
        self.hands_Params.grid(row=0, column=2)

        self.center = ctk.CTkButton(self, command=self.center_cam)
        self.center.grid(row=0, column=4)
        # self.center.onchange()

    def center_cam(self):
        try:
            print("Centrado activo")
            esp32_object.center_image()
        except:
            pass

class web_Cam(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.video_frame=ctk.CTkFrame(self, width=800, height=600)

        self.video_frame.pack()
        self.label = ctk.CTkLabel(self.video_frame, text= " ")
        self.label.pack()
        #self.label.bind("<Motion>", self.mouse)
        self.update_frame()

        self.config = hands_Parameters_config(self)

    def mouse(self, e):
        print(e)

    def get_Cam(self):
        return cam

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

