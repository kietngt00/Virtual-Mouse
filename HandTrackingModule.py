import cv2
import mediapipe as mp
import math

class HandDectector():
    def __init__(self, mode=False, max_hand = 2, detectionCon = 0.5, trackingCon = 0.5):
        self.mpHand = mp.solutions.hands
        self.Hands = self.mpHand.Hands(mode,max_hand,detectionCon,trackingCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.Hands.process(imgRGB)
        if self.result.multi_hand_landmarks and draw == True:
            for handLms in self.result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        h,w,c = img.shape
        self.lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                cx = int(lm.x*w)
                cy = int(lm.y*h)
                self.lmList.append((id,cx,cy))
        return self.lmList

    def openFingers(self, handNo=0):
        tipsId = [4, 8, 12, 16, 20]
        fingers = []
        leftHand = False
        if self.lmList[tipsId[0]-2][1] > self.lmList[tipsId[2]-2][1]:
            leftHand = True
        if self.lmList[tipsId[0]][1] < self.lmList[tipsId[0] - 1][1]:  # thumb close
            if leftHand:
                fingers.append(0)
            else:
                fingers.append(1)
        else:
            if leftHand:
                fingers.append(1)
            else:
                fingers.append(0)

        for i in range(1,5):
            if self.lmList[tipsId[i]][2] < self.lmList[tipsId[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, img, p1, p2, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        length = math.hypot(x2-x1, y2-y1)
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            cv2.circle(img, (x1,y1), 10, (255,255,0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (255,255,0), cv2.FILLED)
        return length, img, x1, x2, y1, y2


