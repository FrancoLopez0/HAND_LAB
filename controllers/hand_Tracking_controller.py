import cv2
import mediapipe as mp
from PIL import Image as Img
from PIL import ImageTk
from entities.classes.Hands import *

program_name = "Handler"

class hand_Tracking_controller(Hands):
    def __init__(self, lbl_video):
        super().__init__()
        self.lbl_video = lbl_video

    def run(self):
        while True:
            ret, self.frame_0 = self.cap.read()

            if ret:
                self._program_()
            else:
                print("No se puede recibir el fotograma")
                break
            cv2.imshow(program_name+'_0', self.frame_0)
            cv2.imshow(program_name, self.frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

    def _window_(self):
        cv2.namedWindow(program_name)
        cv2.namedWindow(program_name + '_0')
        cv2.namedWindow(program_name + ' config')
        
        cv2.createTrackbar('Square', program_name + ' config', self.w_square, 100, self.on_change_square)
        cv2.createTrackbar('Max distance', program_name + ' config', int(self.long_activate * (100/self.height)), 100, self.on_change_distance)
        #cv2.createButton("Show grid", self.btn_grid, None, cv2.QT_RADIOBOX, 0)
        #cv2.putText(self.frame_0, self.long_act > self.long_activate if str('Tracking ON') else str('Tracking OFF'), (self.width-300, self.height-50) ,self.font, 1, color= (self.long_act > self.long_activate if green else red), thickness=2)
        cv2.setMouseCallback(program_name + '_0', self.click_event)
    
    def set_Tracking(self, bool):
        self.tracking = bool

    def show_grid_command(self, bool):
       self.show_square = bool

    def change_Square(self, value):
        self.w_square = value
    
    def change_Distance(self, value):
        self.long_activate = int((100-value) * self.height/100 * 0.3) 

    def get_Square(self):
        return self.w_square

    def get_distance(self):
        return self.long_activate

    def btn_grid(self, *args):
        self.show_square = not self.show_square

    def on_change_square(self,val):
        self.w_square = val
    
    def on_change_distance(self, val):
        self.long_activate = int((100-val) * self.height/100 * 0.3) 
    
    def click_event(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.show_square = not self.show_square
    
    def _program_(self):
        self.frame = self.CamFilter(self.frame_0)
        self.frame_0 = cv2.cvtColor(self.frame_0, cv2.COLOR_BGR2RGB)

        for i,state in enumerate(self.finger_states):
            cv2.circle(self.frame_0, (100+(i*20),50), 3, green if state==1 else red, 3)

        cv2.circle(self.frame_0, (100+(len(self.finger_states)*20),50), 3, green if self.thumb==1 else red, 3)
            
        #self.frame_0 = imutils.resize(self.frame_0, width=640)
        self.Update_Fingers_states(self.frame)

        if(self.Action(self.frame_0) or self.show_square):
            self.Draw()    

#HandsMain(1)
#App()