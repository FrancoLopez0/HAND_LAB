import cv2
#from pyzbar.pyzbar import decode
#from PIL import Image
import math
import numpy as np
import time
import requests

#COLORS
red = (48,48,248)
green = (155,239,91)

class Esp32Cam():
    def __init__(self, url: str = 'http://192.168.4.1'):
        print(f"Init esp32 cam with url: {url}")
        self.url = url
        
        self.set_time(100)

    def isOpened(self):
        response = requests.get(f'{self.url}/pos') #abrimos el URL
        return response.ok

    def set_time(self, time: int):
        try:
            time = int(time)
        except (ValueError, TypeError):
            return False
        response = requests.post(f'{self.url}/time', json={
            'time': time
        })

        print(f'Cambio de tiempos en inicio {response.ok}: {response.text}')

        return response.ok

    def read(self):
        response = requests.get(self.url) #abrimos el URL
        if not response.ok:
            print("Error al obtener la imagen", response.status_code, response.text)
            return False, []
        img_np = np.array(bytearray(response.content),dtype=np.uint8)

        img = cv2.imdecode(img_np,-1) #decodificamos
        return True, img

    def get_cam_position(self):
        response = requests.get(f'{self.url}/pos') #abrimos el URL
        if not response.ok:
            print("Error al obtener la imagen", response.status_code, response.text)
            return response.status_code
        servo_pos = response.json()
        return servo_pos

    def send_coords(self, coords):
        print(self.get_cam_position())
        x = int(-coords[0] / 10)
        y = int(-coords[1] / 5)

        r = requests.post(f'{self.url}/move', json={
            "X": x,
            "Y": y,
        })

        return r.status_code == 200
    
    def release(self):
        return

class CAM():

    def __init__(self, cap):
        self.cap = cap
        
        self.color_lines = green
        self.color_square = self.color_lines
        self.show_square = False

        if not self.cap.isOpened():
                print("No se puede abrir la camara")
                exit()
        
        ret,self.frame_0 = self.cap.read()
        #self.frame_0 = cv2.cvtColor(self.frame_0, cv2.COLOR_BGR2RGB)
        self.w_square = 30
        self.height, self.width = self.frame_0.shape[:2]

    def change_Cam(self, choice):
        #self.__init__(choice)
        self.cap.release()
        self.cap = cv2.VideoCapture(choice)
        ret,self.frame_0 = self.cap.read()

    def CamFilter(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.GaussianBlur(frame, (5, 5), 0)
        frame = cv2.bilateralFilter(frame,15,80,80)
        #_,frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)

        return frame
    
    def Draw(self):
        
        self.frame_0 = self.DrawCross(self.frame_0, self.width, self.height, self.color_lines)
        self.frame_0 = self.DrawSquare(self.frame_0, self.width, self.height, self.color_square)

        #print(height/2, width/2)
        return
    
    def DrawCross(self, frame, width, height, color_lines):
        cv2.line(frame, (int(width/2),0), (int(width/2),height),color_lines,1)
        cv2.line(frame, (0,int(height/2)), (width,int(height/2)),color_lines,1)

        return frame
    
    def DrawSquare(self, frame, width, height, color_square):
        '''
        frame       : image to work
        width       : camera width
        height      : camera height
        color_square: color
        w_square    : square width
        '''
        
        x1 = int(width - width/2 - self.w_square)
        y1 = int(height - height/2 -self.w_square)

        x2 = int(x1 + 2*(self.w_square))
        y2 = int(y1 + 2*(self.w_square))

        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color_square, 2)

        return frame