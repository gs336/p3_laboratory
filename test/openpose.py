import cv2
import mediapipe as mp
import time
import detect
import os
mp_drawing = mp.solutions.drawing_utils
mp_pose=mp.solutions.pose
pose=mp_pose.Pose()
conn=mp.solutions.pose.POSE_CONNECTIONS
def putText(source, x, y, text, scale=2.5, color=(0,0,255)):
    org = (x,y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace, fontScale, color, thickness, lineType)

a=0
n=0
body=0
drawing_spece1=mp_drawing.DrawingSpec(color=(255,255,255),thickness=3,circle_radius=3)
drawing_spece2=mp_drawing.DrawingSpec(color=(255,255,0),thickness=3,circle_radius=3)
cap=cv2.VideoCapture(0)
cap.set(3,1980)
cap.set(4,960)



while cap.isOpened():
    ret ,frame=cap.read()

    
    if not ret:
        print('no camera')
        continue
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    w = int(frame.shape[1]*0.5)
    h = int(frame.shape[0]*0.5)
    frame=cv2.resize(frame,(w,h))
    results=pose.process(image)
    if results.pose_landmarks:
        #mp_drawing.draw_landmarks(frame,results.pose_landmarks,conn,drawing_spece1,drawing_spece2)

        #print(results.pose_landmarks)
        for i in results.pose_landmarks.landmark:
            #if i.visibility>0:
             #   body=body+1
            if i.visibility>=0.7 and i.visibility <1:
                body=body+1
            
            else:
                body=0
        
    if body>1010 and body <1040:
        a = 1             
        sec = 6
 
    if a == 0:
        output = frame.copy() 
    else:
        if body >= 1000 :
            output = frame.copy()
            photo = frame.copy()
            sec = sec - 0.05       
            putText(output, 10, 70, str(int(sec)))
            if sec < 1:
                #output = cv2.addWeighted(white, a, photo, 1-a, 0) 
                a = a - 0.25
                if a<=0:
                    a = 0
                    n = n + 1
                    body=0
                    t=time.strftime("%Y%m%d.%H%M")
                    os.mkdir('../photograph'+'/'+f'{t}')
                    cv2.imwrite('../photograph'+'/'+f'{t}'+'/'+f'photo-{n}.jpg', photo)
                    putText(output, 10, 70,'Save OK')   # 存檔
                    print('save ok')    
                    # opt = detect.parse_opt()
                    # detect.main(opt)  


        else:
            a = 0
            pass
    

    print(body,'xxx',a)
    cv2.imshow('111',output)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()