import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon= 0.8)
colorR = (255,0,255)

cx,  cy, w, h  = 100, 100, 200, 200


class DragRect():
    def __init__(self,posCentre, size=[200,200]):
        self.posCentre = posCentre
        self.size = size

    def update(self,cursor):                                                                #upadting the position

        cx,cy = self.posCentre
        w,h = self.size

                                                                                            #if the index tip finger is in Rectange region

        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCentre = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)  #index No:1
    img = detector.findHands(img)
    lmList, _= detector.findPosition(img)

    if lmList:                                                                                 #Checking the point of finger
        l, _, _ = detector.findDistance(8,12, img,draw = False)                                #To check , finding a Distance of Index steps
        print(l)

        if l<30:
            cursor = lmList[8]                                                                 # index finger tip landmark
            # Call the update

            for rect in rectList:
                rect.update(cursor)

        ##Draw  solid

        for rect in rectList:
            cx, cy = rect.posCentre
            w, h= rect.size
            cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2)
                         ,colorR, cv2.FILLED)
            cvzone.cornerRect(img, (cx-w //2, cy-h //2,w,h),20,rt = 0)                          #(x1,x2) (y1,y2)

    cv2.imshow("Img",img)
    cv2.waitKey(1)
