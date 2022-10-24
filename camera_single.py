# camera_single.py

import detect
import cv2
import mediapipe as mp
import time
from datetime import datetime
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
drawing_spece1=mp_drawing.DrawingSpec(color=(255,255,255),thickness=3,circle_radius=3)#openpose 骨架顏色
drawing_spece2=mp_drawing.DrawingSpec(color=(255,255,0),thickness=3,circle_radius=3)#openpose 骨架顏色

# UDP_URL='udp://127.0.0.1:8066'#server端ip位置 port自訂

class Camera():

    def __init__(self):
        
        # self.video = cv2.VideoCapture(UDP_URL,cv2.CAP_FFMPEG) #server接收client的影像
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
        #image = cv2.resize(image, (960, 640), interpolation=cv2.INTER_AREA)
        image1=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results=pose.process(image1)
        #image=cv2.resize(image,(640,480),interpolation=cv2.INTER_AREA)
        
        if self.n==0:#n=0時間就會一直刷新
            localtime=time.localtime()
            detect.t=time.strftime('%Y%m%d_%H%M%S',localtime)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image,results.pose_landmarks,conn,drawing_spece1,drawing_spece2)#顯使骨架

            for i in results.pose_landmarks.landmark:
                print(F'[DEBUG] i.visibility: {i.visibility}; self.body: {self.body};self.prev_time:{self.prev_time}')
                #visibility=偵測到的特徵點數目/33
                if i.visibility>=0.1 and i.visibility <1:#visibility大於0.5開始累加參數
                    self.body=self.body+1#若FPS為10，偵測到的特徵點數目為33，body每秒就會加330
                    
                else:
                    self.body=0#若累加途中visibility降至0.5以下body直接歸0
        if self.body>=0 and self.body<25:#當body累加至1010與1040間(大約累加2~3秒)
           self.a=1#a=1即達成倒數計時的其中一個條件
           self.sec=6#sec預設為6
           self.prev_time = datetime.now()
           
        if self.a!=0 and self.body>=0:#兩個條件都達到就會開始倒數計時
            
            self.timedalta = datetime.now() - self.prev_time
            putText(image,10,70,str(int(self.timedalta.seconds)))#秒數顯示於營幕上
            if self.timedalta.seconds >=5:
                self.a=self.a-0.25
                if self.a<=0:
                    self.a=0
                    self.n=self.n+1#n變成一後就不會累加時間
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


