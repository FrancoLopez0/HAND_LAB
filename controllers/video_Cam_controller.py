import subprocess
import re
import cv2
from entities.classes.Hands import Hands

class video:
    def __init__(self):
        pass
    
    def get_available_video(self):

        command = ['wmic', 'path', 'Win32_PnPEntity', 'where', 'Caption like "%(video)%"', 'get', 'Caption']
        result = subprocess.run(command, capture_output=True, text=True)
        status = re.split(r"\n\n", result.stdout)[1:]
        content = [
                    {cont[0].strip(): cont[1].strip() 
                        for line in lines if len(cont := line.split(':')) == 2
                    } 
                   for video in status if (lines := video.split('\n'))[0]]
        return content
    
    def list_availables_cam(self,max_camaras=10):
        availables_cam = []
        for i in range(max_camaras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                availables_cam.append(i)
                cap.release()
        availables_cam = [str(x) for x in availables_cam]
        return availables_cam
    
    def change_cam(self, object:Hands, cam):
        object.change_Cam(cam)
        