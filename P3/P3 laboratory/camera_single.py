# camera_single.py

import detect
import cv2
import mediapipe as mp
import time
import os


#def顯示文字之function
def putText(source, x, y, text, scale=2.5, color=(0,0,255)):
    org = (x,y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace, fontScale, color, thickness, lineType)
mp_drawing = mp.solutions.drawing_utils
mp_pose=mp.solutions.pose
pose=mp_pose.Pose()
conn=mp.solutions.pose.POSE_CONNECTIONS
# drawing_spece1=mp_drawing.DrawingSpec(color=(255,255,255),thickness=3,circle_radius=3)#openpose 骨架顏色
# drawing_spece2=mp_drawing.DrawingSpec(color=(255,255,0),thickness=3,circle_radius=3)#openpose 骨架顏色

#UDP_URL='udp://10.66.203.119:8066'#server端ip位置 port自訂

class Camera():

    def __init__(self):
        
        #self.video = cv2.VideoCapture(UDP_URL,cv2.CAP_FFMPEG) #server接收client的影像
        self.video = cv2.VideoCapture(0) #camera於server開啟

        self.video.set(3,1280)
        self.video.set(4,640)
        self.body=0
        self.a=0
        self.n=0
        self.sec=6
        # self.t=float(time.strftime("%Y%m%d.%H%M%S"))

    def __del__(self):
        self.video.release()

    def get_frame(self):

        success, image = self.video.read()
        image = image[115:865,340:940]
        # image = cv2.resize(image, (960, 640), interpolation=cv2.INTER_AREA)
        image1=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results=pose.process(image1)
        #image=cv2.resize(image,(640,480),interpolation=cv2.INTER_AREA)
        
        if self.n==0:
            localtime=time.localtime()
            detect.t=time.strftime('%Y%m%d_%H%M%S',localtime)

        if results.pose_landmarks:
            #mp_drawing.draw_landmarks(image,results.pose_landmarks,conn,drawing_spece1,drawing_spece2)#顯使骨架

            for i in results.pose_landmarks.landmark:
                if i.visibility>=0.5 and i.visibility <1:
                    self.body=self.body+1
                    
                else:
                    self.body=0
        if self.body>1010 and self.body<1040:
           self.a=1
           self.sec=6
           
           
        if self.a==0:
            pass
                
        else:
            if self.body>=1000:
                self.sec=self.sec-0.05
                putText(image,10,70,str(int(self.sec)))  
                if self.sec<1:
                    self.a=self.a-0.25
                    if self.a<=0:
                        self.a=0
                        self.n=self.n+1
                        self.body=100   
                        
                        if self.n==1:
                            os.mkdir('../photograph'+'/'+f'{detect.t}')
                            cv2.imwrite('../photograph'+'/'+detect.t+'/'+f'photo-{self.n}.jpg', image)
            
                        else:
                            cv2.imwrite('../photograph'+'/'+detect.t+'/'+f'photo-{self.n}.jpg', image)
    
                        putText(image, 10, 70,'Save OK')   # 存檔
                        print('save ok') 

                        if self.n==2:
                            
                            ###啟動detect
                            opt = detect.parse_opt()
                            detect.main(opt)  
                            ###
                            self.n=0             

            else:
                self.a=0
                
                pass
        
        
        #print(self.body,'xxx',self.a)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


