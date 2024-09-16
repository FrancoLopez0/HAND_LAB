import cv2
#from pyzbar.pyzbar import decode
#from PIL import Image
import math
import numpy as np
import time

#COLORS
red = (48,48,248)
green = (155,239,91)

class Control():
    def __init__(self):
        print("Control")
    
    def SendDistance(x,y):
        
        print("Distance x: ", x)
        print("Distance y: ", y)

        return

class CAM():
    def __init__(self, cam_selected = 0):

        self.cap = cv2.VideoCapture(cam_selected)
        
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