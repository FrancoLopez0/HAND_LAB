import cv2
import mediapipe as mp
import imutils
from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
from classes.Hands import *

program_name = "Handler"

class App():
    def __init__(self) -> None:
        
        root = Tk()

        btn_init = Button(root, text="Init", width=45, command=self.init)
        btn_init.grid(column=0,row=0,padx=5,pady=5)

        btn_exit = Button(root, text="Exit", width=45)
        btn_exit.grid(column=1, row=0, padx=5, pady=5)

        self.lbl_video = Label(root)
        self.lbl_video.grid(column=0, row=1, columnspan=2)

        root.mainloop()
    
    def init(self):
        HandsMain(self.lbl_video)

class HandsMain(Hands):
    def __init__(self, lbl_video):
        super().__init__()
        self.lbl_video = lbl_video

        self._window_()

        #self._visualizar_()

        while True:
            ret, self.frame_0 = self.cap.read()

            if ret:
                self._program_()
                #self.points_ant = self.p1
                #im = Image.fromarray(self.frame_0)
                #img = ImageTk.PhotoImage(image=im)

                #self.lbl_video.configure(image = img)
                #self.lbl_video.image = img
                
            else:
                print("No se puede recibir el fotograma")
                break
            cv2.imshow(program_name+'_0', self.frame_0)
            cv2.imshow(program_name, self.frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
    
    def _visualizar_(self):
        #ret, self.frame_0 = self.cap.read()
        ret, frame = self.cap.read()
        
        print(ret)

        if ret:
            #self._program_()
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #self.points_ant = self.p1
            im = Img.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            self.lbl_video.configure(image = img)
            self.lbl_video.image = img
            self.lbl_video.after(10, self._visualizar_)
                
        else:
            self.lbl_video.image = ""
            self.cap.release()
            print("No se puede recibir el fotograma")

    def _window_(self):
        cv2.namedWindow(program_name)
        cv2.namedWindow(program_name + '_0')
        cv2.namedWindow(program_name + ' config')
        
        cv2.createTrackbar('Square', program_name + ' config', self.w_square, 100, self.on_change_square)
        cv2.createTrackbar('Max distance', program_name + ' config', int(self.long_activate * (100/self.height)), 100, self.on_change_distance)
        #cv2.createButton("Show grid", self.btn_grid, None, cv2.QT_RADIOBOX, 0)
        #cv2.putText(self.frame_0, self.long_act > self.long_activate if str('Tracking ON') else str('Tracking OFF'), (self.width-300, self.height-50) ,self.font, 1, color= (self.long_act > self.long_activate if green else red), thickness=2)
        cv2.setMouseCallback(program_name + '_0', self.click_event)

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
        self.frame_0 = imutils.resize(self.frame_0, width=640)
        self.Update_Fingers_states(self.frame)
        if(self.Action(self.frame_0) or self.show_square):
            self.Draw()    

HandsMain(1)
#App()