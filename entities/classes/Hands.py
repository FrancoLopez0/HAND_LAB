from time import sleep
from entities.classes.Cam import *
import mediapipe as mp
import numpy
import requests
from math import degrees, acos


class Hands(CAM):
    def __init__(self, cap: int = 0):
        super().__init__(cap)

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.tracking = True

        self.max_long_activate = 0.15
        self.min_long_activate = 0.10
        self.current_long = 0

        self.up = [240, 256, 243, 210]
        self.up_thumb = 170
        self.down_thumb = 100
        self.down = [103, 90, 80, 77]
        self.up_down = [up - down for up, down in zip(self.up, self.down)]
        self.up_down_thumb = self.up_thumb - self.down_thumb
        self.norm = []
        self.norm_thumb = 0

        self.fingertips_points = [8, 12, 16, 20]
        self.base_fingers_points = [6, 10, 14, 18]
        self.palm_points = [0, 1, 5, 9, 13, 17]
        self.thumb_points = [1, 2, 4]
        self.coords_thumb = []
        self.coords_points_palm = []
        self.coords_base_fingers_points = []
        self.palm_centroid = []
        self.coords_tips = []
        self.finger_states = [0, 0, 0, 0]
        self.thumb = 0
        self.dentro_del_cuadrado = None
        self.ant_states = [1, 1, 1, 1]
        self.inter_states = [0, 0, 0, 0]

        self.points_ant = []
        self.p1 = []

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        self.results = None

        self.point = self.mp_hands.HandLandmark
        self.points = None

        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75)

        self.coords2send = []

    def HandsObtainCoords(self, frame):
        self.results = self.hands.process(frame)

        if self.results.multi_hand_landmarks is not None:

            self.coords_tips = []
            self.coords_base_fingers_points = []
            self.coords_thumb = []
            self.base = []

            for hand_landmarks in self.results.multi_hand_landmarks:

                self.current_long = hand_landmarks.landmark[5].x - \
                    hand_landmarks.landmark[17].x

                # print(self.current_long)

                x_base = int(hand_landmarks.landmark[0].x * self.width)
                y_base = int(hand_landmarks.landmark[0].y * self.height)

                self.base.append([x_base, y_base])

                # print(self.base)

                for finger_point in self.fingertips_points:
                    x = int(
                        hand_landmarks.landmark[finger_point].x * self.width)
                    y = int(
                        hand_landmarks.landmark[finger_point].y * self.height)
                    # cv2.circle(frame,(x,y), 5, (0, 255, 0), -1)
                    self.coords_tips.append([x, y])

                for finger_point in self.base_fingers_points:
                    x = int(
                        hand_landmarks.landmark[finger_point].x * self.width)
                    y = int(
                        hand_landmarks.landmark[finger_point].y * self.height)
                    # cv2.circle(frame,(x,y), 5, (0, 0, 255), -1)
                    self.coords_base_fingers_points.append([x, y])

                for palm_point in self.palm_points:
                    x = int(hand_landmarks.landmark[palm_point].x * self.width)
                    y = int(
                        hand_landmarks.landmark[palm_point].y * self.height)
                    # cv2.circle(frame,(x,y), 5, (0, 255, 0), -1)
                    self.coords_points_palm.append([x, y])

                for thumb_point in self.thumb_points:
                    x = int(
                        hand_landmarks.landmark[thumb_point].x * self.width)
                    y = int(
                        hand_landmarks.landmark[thumb_point].y * self.height)
                    # cv2.circle(frame,(x,y), 5, (0, 255, 0), -1)
                    # print((x,y))
                    self.coords_thumb.append([x, y])
            return
        else:
            self.coords_tips = []
            self.coords_base_fingers_points = []
            self.coords_points_palm = []
            self.coords_thumb = []
            self.base = []

    def Update_Fingers_states(self, frame):
        self.HandsObtainCoords(frame)
        if (self.coords_base_fingers_points != [] and self.current_long < self.max_long_activate and self.current_long > self.min_long_activate):
            for i in range(len(self.fingertips_points)):
                if (self.coords_base_fingers_points[i][1] > self.coords_tips[i][1]):
                    # Dedo arriba
                    self.finger_states[i] = 1
                else:
                    self.finger_states[i] = 0
        try:
            if (len(self.coords_thumb) >= 3):
                p = [np.array(point) for point in self.coords_thumb]

                l1 = np.linalg.norm(p[1]-p[2])
                l2 = np.linalg.norm(p[0]-p[2])
                l3 = np.linalg.norm(p[0]-p[1])

                angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2*l1*l3)))

                self.thumb = 1 if angle >= 130 else 0

                angle -= self.down_thumb

                self.norm_thumb = (angle / self.up_down_thumb if angle /
                                   self.up_down_thumb > 0 else 0) if angle/self.up_down_thumb < 1 else 1

        except Exception as e:
            print('Error in thumb:', e)

        try:
            if (len(self.base)):
                p_tips = [np.array(point) for point in self.coords_tips]
                p_base = np.array(self.base)

                l_base = [float(np.linalg.norm(point_tip - p_base))
                          for point_tip in p_tips]

                mod = [current - down for current,
                       down in zip(l_base, self.down)]

                self.norm = [((current / up_down if current/up_down > 0 else 0)if current / up_down < 1 else 1) for current,
                             up_down in zip(mod, self.up_down)]

        except:
            pass
        # print(self.finger_states)
        # print(self.coords_base_fingers_points)

    def sendFingerStates(self):
        if (self.coords_tips != [] and self.current_long < self.max_long_activate and self.current_long > self.min_long_activate):  # If hand has detected
            try:
                url = "http://192.168.1.1"
                # params = {
                #     'thumb': 'up' if self.thumb == 1 else 'down',
                #     'index': 'up' if self.finger_states[0] == 1 else 'down',
                #     'middle': 'up' if self.finger_states[1] == 1 else 'down',
                #     'ring': 'up' if self.finger_states[2] == 1 else 'down',
                #     'pinky': 'up' if self.finger_states[3] == 1 else 'down',
                # }
                params = {
                    'thumb': str(round(self.norm_thumb, 2)),
                    'index': str(round(self.norm[0], 2)),
                    'middle': str(round(self.norm[1], 2)),
                    'ring': str(round(self.norm[2], 2)),
                    'pinky': str(round(self.norm[3], 2)),
                }

                print(f'send {params}')
                r = requests.get(url, params)
            except:
                print("Error")

    def Action(self, frame):

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"long: {round(self.current_long, 3)}",
                    (100, 500), font, 0.5, (0, 0, 0), 2)

        if (self.coords_tips != [] and self.current_long < self.max_long_activate and self.current_long > self.min_long_activate):  # If hand has detected

            dentro_del_cuadrado = (int(self.width - self.width/2 + self.w_square) > self.coords_tips[0][0]) and (
                self.coords_tips[0][0] > int(self.width - self.width/2 - self.w_square))
            dentro_del_cuadrado = dentro_del_cuadrado and (int(self.height - self.height/2 + self.w_square) > self.coords_tips[0][1]) and (
                self.coords_tips[0][1] > int(self.height - self.height/2 - self.w_square))

            for coords in self.coords_tips:
                cv2.circle(frame, coords, 3, green, -1)

            try:
                for coords in self.coords_thumb:
                    cv2.circle(frame, coords, 3, green, -1)
            except:
                pass

            if (self.finger_states == [1, 0, 0, 0] and not dentro_del_cuadrado and self.tracking):
                try:
                    cv2.circle(frame, self.coords_tips[0], 5, red, -1)
                    cv2.line(frame, self.coords_tips[0], (int(
                        self.width/2), int(self.height/2)), red, 2)

                    self.coords2send = [self.coords_tips[0][0] - int(
                        self.width/2), (self.coords_tips[0][1] - int(self.height/2))*(-1)]

                    cv2.putText(frame, f"{self.coords2send}", (
                        self.coords_tips[0][0] + 10, self.coords_tips[0][1]), font, 0.5, green, 2)

                except:
                    return False
                return True
            # self.ant_states = self.finger_states
        return False

    def detect_f3_fingers_down(self):

        if self.coords_tips and self.finger_states == [1, 1, 0, 0] and self.thumb:
            return True
        return False

    def Palm_centroid(self, frame):
        prom_x = 0
        prom_y = 0
        print(self.coords_points_palm)
        if (self.coords_points_palm != []):
            coords = np.array(self.coords_points_palm)
            # print(coords)
            # print(self.palm_points)
            self.palm_centroid = np.mean(coords, axis=0)
            self.palm_centroid = (
                int(self.palm_centroid[0]), int(self.palm_centroid[1]))
            cv2.circle(self.frame, self.palm_centroid, 10, (255, 0, 0), -1)
