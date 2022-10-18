import cv2
import socket

# addr=('10.66.202.97',8066)
addr=('127.0.0.1',8066)

cap=cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,960)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    ret, frame=cap.read()
    frame=cv2.resize(frame,(640,480),interpolation=cv2.INTER_AREA)
    _,send_data=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,50])
    s.sendto(send_data,addr)
    cv2.imshow('ckient',frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cv2.destroyAllWindows()
s.close()