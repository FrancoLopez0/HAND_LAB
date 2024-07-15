import cv2
import mediapipe as mp
from classes.Hands import *
program_name = "Handler"

class HandsMain(Hands):
    def __init__(self):
        super().__init__()
        cv2.namedWindow(program_name)
        cv2.namedWindow(program_name + '_0')
        
        cv2.createTrackbar('Square', program_name + '_0', 0, 100, self.on_change)
        cv2.setMouseCallback(program_name + '_0', self.click_event)

        while True:
            ret, self.frame_0 = self.cap.read()

            if ret:
                self.frame = self.CamFilter(self.frame_0)
                self.Update_Fingers_states(self.frame)
                if(self.Action(self.frame_0) or self.ShowSquare):
                    self.Draw()           
                self.points_ant = self.p1
            
            else:
                print("No se puede recibir el fotograma")
                break
            cv2.imshow(program_name+'_0', self.frame_0)
            cv2.imshow(program_name, self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
    
    def on_change(self,val):
        self.w_square = val
    
    def click_event(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ShowSquare = not self.ShowSquare
HandsMain()