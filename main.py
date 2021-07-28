from typing import MutableMapping
import cv2
import mediapipe as mp
import time
import HandTrackingModule as HTM
import numpy as np
import pyautogui as pag

##################################
wCap, hCap = 640, 480
wScr, hScr = pag.size()

xFrame1, yFrame1 = 100, 100
xFrame2, yFrame2 = 540, 330

smoothFactor = 5
#################################
cap = cv2.VideoCapture(0)
cap.set(3, wCap)
cap.set(4, hCap)

detector = HTM.HandDectector(max_hand=1, detectionCon=0.7)

xmPrev = 0
ymPrev = 0

pTime = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHand(img)

    cv2.rectangle(img, (xFrame1,yFrame1), (xFrame2,yFrame2), (255,0,255), 3)

    # 1. Find which fingers are open: need locations of all landmarks
    lmList = detector.findPosition(img)
    if len(lmList) > 0:
        fingers = detector.openFingers()
        count = fingers.count(1)
        # 2. Check move mouse mode: only index finger opens
        if fingers[1]:
            # 2.0 Convert move frame
            x1, y1 = lmList[8][1:]
            cv2.circle(img, (x1,y1), 10, (255,255,0), cv2.FILLED)
            if x1>xFrame1 and x1<xFrame2 and y1>yFrame1 and y1<yFrame2:
                xm = np.interp(x1, (xFrame1,xFrame2), (0,wScr))
                ym = np.interp(y1, (yFrame1,yFrame2), (0,hScr))
                # 2.2 Smoothen the movement
                xm = xmPrev + (xm-xmPrev)/smoothFactor
                ym = ymPrev + (ym-ymPrev)/smoothFactor
                xmPrev, ymPrev = xm, ym
                # 2.1 Move mouse
                if count==1:
                    pag.moveTo(xm,ym,_pause=False)

            # 3. Check click mode: only index finger and middle finger open
                elif fingers[2] and count == 2:
                    length, img, x1, x2, y1, y2 = detector.findDistance(img,8,12)
                #3.1 Single click: 2 fingers are closed
                    if 20<length and length<27 and y1>y2: # Left click
                        pag.click(xm,ym,interval=0.2,_pause=False)
                    elif length<17 and y1<y2:       # Right click
                        pag.rightClick(xm,ym,interval=0.2,_pause=False)
                # 3.2 Double click: 2 fingers are far
                    elif x1-x2>90 or x2-x1>90:
                        pag.doubleClick(xm,ym,interval=0.2,_pause=False)

            # 4. Scroll mode:
                # Sroll up: thumb and index fingers are open
                elif fingers[0] and count == 2:
                    pag.scroll(5,_pause=False)
                # Scroll down: thumb, index and middle fingers are open
                elif fingers[0] and fingers[2] and count == 3:
                    pag.scroll(-5,_pause=False)

    # Frame 
    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    cv2.putText(img, str(fps), (30,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

    # Display
    cv2.imshow("Capture", img)
    key = cv2.waitKey(1)

    # Exit
    if key == 27: # ESC key
        break