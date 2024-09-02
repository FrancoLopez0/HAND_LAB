import cv2
import mediapipe as mp
from classes.Hands import *

from time import sleep
from classes.wifi import WifiManager
wifi_manager = WifiManager()
program_name = "Handler"

url = 'http://192.168.4.1'
wifi_name = 'Esp32 Access point'

def main():
    HandsMain()

class HandsMain(Hands):
    def __init__(self):
        esp32_object = Esp32Cam() if wifi_manager.is_connected(wifi_name) else None
        if esp32_object:
            capture_object = esp32_object
        else:
            capture_object = cv2.VideoCapture(0)
    
        super().__init__(capture_object)
        self.esp_cam = esp32_object
        self.start()

    def start(self):
        cv2.namedWindow(program_name)
        
        cv2.createTrackbar('Square', program_name, 0, 100, self.on_change)
        cv2.setMouseCallback(program_name, self.click_event)

        while True:
            ret, self.frame_0 = self.cap.read()


            if ret:
                self.frame = self.CamFilter(self.frame_0)
                self.Update_Fingers_states(self.frame)
                if(self.Action(self.frame_0) or self.ShowSquare):
                    self.Draw()
                    # print(self.coords2send)
                    if self.esp_cam:
                        self.esp_cam.send_coords(self.coords2send)
                self.points_ant = self.p1
            
                
            else:
                print("No se puede recibir el fotograma")
                break
            cv2.imshow(program_name, self.frame_0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
    
    def on_change(self,val):
        self.w_square = val
    
    def click_event(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ShowSquare = not self.ShowSquare

if __name__ == '__main__':
    main()