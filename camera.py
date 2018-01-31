# -*- coding: utf-8 -*-
import sys, os
import time
from datetime import datetime
import cv2

_W = 320
_H = 240
cycle = 30

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

imglist = []
maplist = []
imglist.append(cv2.imread("1.png"))
imglist.append(cv2.imread("2.png"))
imglist.append(cv2.imread("3.png"))
maplist.append(cv2.imread("m1.png"))
maplist.append(cv2.imread("m2.png"))

count = 0
lost_count = 0
current = 0
isAppear = False
touch_width = 0
over = None

cap = cv2.VideoCapture(0)

while True:
    print(lost_count)
    ret, im = cap.read()
    image = cv2.flip(im, 1)

    count += 1
    if count >= cycle:
        count = 0
        current = 0 if current == len(imglist)-1 else current+1

    width, height = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # over = cv2.resize(imglist[current], (880,720))
    # image[0:720,400:1280] = over

    if lost_count > 0:
        lost_count = 0 if lost_count >= 30 else lost_count + 1

    if len(faces) == 0:
        if isAppear :
            lost_count = 1
            isAppear = False
        if lost_count == 0 :
            over = cv2.resize(imglist[current], (880,720))
    else:
        isAppear = True

    rect1 = (100, 100, 300, 200)
    cv2.rectangle( image, (rect1[0],rect1[1]), (rect1[2], rect1[3]), (0, 100, 0), -1)
    cv2.putText(image, "Korimoto", (rect1[0]+20,rect1[1]+(rect1[3]-rect1[1])/2), 1, 2, (0,0,200), 2)
    rect2 = (100, 300, 300, 400)
    cv2.rectangle( image, (rect2[0],rect2[1]), (rect2[2], rect2[3]), (0, 100, 0), -1)
    cv2.putText(image, "Sakuragaoka", (rect2[0]+20,rect2[1]+(rect2[3]-rect2[1])/2), 1, 1.5, (0,0,200), 2)

    for (x, y, w, h) in faces:
        p = (x+w/2, y+h/2)
        if rect1[0] < p[0] and p[0] < rect1[2] and rect1[1] < p[1] and p[1] < rect1[3]:
            lost_count = 1
            cv2.rectangle( image, (rect1[0],rect1[1]), (rect1[2], rect1[3]), (100, 100, 0), -1)
            cv2.putText(image, "Korimoto", (rect1[0]+20,rect1[1]+(rect1[3]-rect1[1])/2), 1, 2, (0,0,200), 2)
            over = cv2.resize(maplist[0], (880,720))
        if rect2[0] < p[0] and p[0] < rect2[2] and rect2[1] < p[1] and p[1] < rect2[3]:
            lost_count = 1
            cv2.rectangle( image, (rect2[0],rect2[1]), (rect2[2], rect2[3]), (100, 100, 0), -1)
            cv2.putText(image, "Sakuragaoka", (rect2[0]+20,rect2[1]+(rect2[3]-rect2[1])/2), 1, 1.5, (0,0,200), 2)
            over = cv2.resize(maplist[1], (880,720))
        if x+w/2 < 400 :
            cv2.circle(image, p, 20, (0,200,0), 3, 4)

        # show the frame
    image[0:720,400:1280] = over
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
