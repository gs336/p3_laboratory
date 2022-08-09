import cv2
from cv2 import VideoCapture

cap=VideoCapture(0)
while(True):
    ret, frame=cap.read()
    cv2.imshow('111',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()