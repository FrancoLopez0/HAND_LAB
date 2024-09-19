import cv2
import mediapipe as mp
from entities.classes.Hands import *
import requests
from time import sleep
program_name = "Handler"

url = 'http://192.168.4.1'

def main():
    # HandsMain(esp_cam=False)
    y = 0
    while((x := input('Pos x: ') )!= 'n'):
        response = requests.get(f'{url}/pos') #abrimos el URL
        print(response.text)
        print(int(x))
        r = requests.post(f'{url}/move', json={
            "X": int(x),
            "Y": y,
        })
        print(r.text)

    x = 0
    while((y := input('Pos y: ')) != 'n'):
        response = requests.get(f'{url}/pos') #abrimos el URL
        print(response.text)
        r = requests.post(f'{url}/move', json={
            "X": x,
            "Y": int(y),
        })
        print(r.text)



def send_coords(coords):
    response = requests.get(f'{url}/pos') #abrimos el URL
    if not response.ok:
        print("Error al obtener la imagen", response.status_code, response.text)
        return response.status_code
    x = int(int(response.json()['move_x']) - coords[0] / 10)
    y = int(int(response.json()['move_y']) - coords[1] / 5)

    r = requests.post(f'{url}/move', json={
        "X": x,
        "Y": y,
    })

    return r.status_code

def read_cam():
    response = requests.get(url) #abrimos el URL
    if not response.ok:
        print("Error al obtener la imagen", response.status_code, response.text)
        return False, []
    img_np = np.array(bytearray(response.content),dtype=np.uint8)

    img = cv2.imdecode(img_np,-1) #decodificamos
    return img

class HandsMain(Hands):
    def __init__(self, esp_cam):
        super().__init__(cap=0)
        self.esp_cam = esp_cam
        self.start()
    
    def start(self):
        cv2.namedWindow(program_name)
        
        cv2.createTrackbar('Square', program_name, 0, 100, self.on_change)
        cv2.setMouseCallback(program_name, self.click_event)

        while True:
            if self.esp_cam:
                ret, self.frame_0 = read_cam()
            else: 
                ret, self.frame_0 = self.cap.read()


            if ret:
                self.frame = self.CamFilter(self.frame_0)
                self.Update_Fingers_states(self.frame)
                if(self.Action(self.frame_0) or self.ShowSquare):
                    self.Draw()
                    # print(self.coords2send)
                    if self.esp_cam:
                        send_coords(self.coords2send)
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