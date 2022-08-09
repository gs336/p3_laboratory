# camera_single.py
from this import d
import detect
import cv2
import mediapipe as mp
import time
import os

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
drawing_spece1=mp_drawing.DrawingSpec(color=(255,255,255),thickness=3,circle_radius=3)
drawing_spece2=mp_drawing.DrawingSpec(color=(255,255,0),thickness=3,circle_radius=3)



class Camera():

    

    def __init__(self):
        
        self.video = cv2.VideoCapture(0)
        self.video.set(3,1280)
        self.video.set(4,960)
        self.body=0
        self.a=0
        self.n=0
        self.sec=6
        # self.t=float(time.strftime("%Y%m%d.%H%M%S"))
        # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ
    

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # t=float(time.strftime("%Y%m%d.%H%M"))
        success, image = self.video.read()
        image = image[115:865,340:940]
        # image = cv2.resize(image, (960, 640), interpolation=cv2.INTER_AREA)
        image1=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results=pose.process(image1)
        if self.n==0:
            localtime=time.localtime()
            detect.t=time.strftime('%Y%m%d_%H%M%S',localtime)

        if results.pose_landmarks:
            #mp_drawing.draw_landmarks(image,results.pose_landmarks,conn,drawing_spece1,drawing_spece2)

            for i in results.pose_landmarks.landmark:
                if i.visibility>=0.7 and i.visibility <1:
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
                    # exec(open('./detect.py').read())
                        # if __name__ == "__main__":
                        if self.n==2:
                            opt = detect.parse_opt()
                            detect.main(opt)  
                            self.n=0             

            else:
                self.a=0
                
                pass
        
        
        #print(self.body,'xxx',self.a)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()




 
    

        # read()は、二つの値を返すので、success, imageの2つ変数で受けています。
        # OpencVはデフォルトでは raw imagesなので JPEGに変換
        # ファイルに保存する場合はimwriteを使用、メモリ上に格納したい時はimencodeを使用
        # cv2.imencode() は numpy.ndarray() を返すので .tobytes() で bytes 型に変換
   
