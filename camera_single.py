# camera_single.py

import detect
import cv2
import mediapipe as mp
import time
from datetime import datetime
import os

COUNT_DOWN_SEC = 5  # 倒數秒數
START_SHOOTING_THRES = 1500  # 如果帶大於該閥值，則開始拍照

# def顯示文字之function


def putText(source, x, y, text, scale=2.5, color=(0, 0, 255)):
    org = (x, y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace,
                fontScale, color, thickness, lineType)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
conn = mp.solutions.pose.POSE_CONNECTIONS
drawing_spece1 = mp_drawing.DrawingSpec(
    color=(255, 255, 255), thickness=3, circle_radius=3)  # openpose 骨架顏色
drawing_spece2 = mp_drawing.DrawingSpec(
    color=(255, 255, 0), thickness=3, circle_radius=3)  # openpose 骨架顏色

# UDP_URL='udp://127.0.0.1:8066'#server端ip位置 port自訂


class Camera():

    def __init__(self):

        # self.video = cv2.VideoCapture(UDP_URL,cv2.CAP_FFMPEG) #server接收client的影像
        self.video = cv2.VideoCapture(0)  # camera於server開啟

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        self.reset()
        # self.t=float(time.strftime("%Y%m%d.%H%M%S"))
        

    def __del__(self):
        self.video.release()
        
    def reset(self):
        self.body = 0   # 身體特徵點，判斷自動拍照用
        self.shooted_num = 0  # 已經拍攝之數量
        self.prev_time = datetime.now()  # 開始拍攝之當下時間，倒數用
        self.is_shooting = False  # 是否進入拍照狀態用?
        self.is_detected = False  # 是否已經檢測完畢?
        self.detected_result = ""

    def get_frame(self):
        _, origin_image = self.video.read()
        crop_image = origin_image[115:865, 340:940]
        crop_image_copy = crop_image.copy()
        #image = cv2.resize(image, (960, 640), interpolation=cv2.INTER_AREA)
        crop_image_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
        results = pose.process(crop_image_rgb)
        # image=cv2.resize(image,(640,480),interpolation=cv2.INTER_AREA)

        if self.shooted_num == 0:  # n=0時間就會一直刷新
            localtime = time.localtime()
            detect.t = time.strftime('%Y%m%d_%H%M%S', localtime)
            self.save_path = os.path.join('../photograph', detect.t)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                crop_image, results.pose_landmarks, conn, drawing_spece1, drawing_spece2)  # 顯使骨架

            for i in results.pose_landmarks.landmark:
                # print(F'[DEBUG] i.visibility: {i.visibility}; self.body: {self.body};self.prev_time:{self.prev_time}')
                # visibility=偵測到的特徵點數目/33
                if i.visibility >= 0.5 and i.visibility < 1:  # visibility大於0.5開始累加參數
                    self.body = self.body + 1  # 若FPS為10，偵測到的特徵點數目為33，body每秒就會加330
                else:
                    self.body = 0  # 若累加途中visibility降至0.5以下body直接歸0
        print(f"[DEBUG] self.body: {self.body}; self.is_shooting: {self.is_shooting}")
        # 當body累加至1010與1040間(大約累加2~3秒)
        if self.body >= START_SHOOTING_THRES and not self.is_shooting:
            self.save_path = ''
            self.is_shooting = True  # Lock status : 開始拍照
            self.prev_time = datetime.now()  # 取得當前之時間
            if self.is_detected:
                self.is_detected = False

        if self.is_shooting and self.body >= 0:  # 兩個條件都達到就會開始倒數計時
            self.timedalta = datetime.now() - self.prev_time
            putText(crop_image, 10, 70, str(COUNT_DOWN_SEC -
                    int(self.timedalta.seconds)))  # 倒數秒數顯示於營幕上
            if self.timedalta.seconds >= COUNT_DOWN_SEC:  # 開始倒數 5 秒，5秒後進入下列拍照流程
                self.prev_time = datetime.now() # Reset time
                self.shooted_num = self.shooted_num + 1  # 拍攝一張， n 變成 1 後就不會累加時間
                self.body = 0  # Reset 成 1 讓該迴圈進行，好拍攝第二張背面照片

                if self.shooted_num == 1:
                    os.mkdir('../photograph'+'/'+f'{detect.t}')
                    cv2.imwrite(os.path.join(self.save_path,
                                             f'photo-{self.shooted_num}.jpg'), crop_image_copy)
                    print(f'[INFO] {detect.t} : front image save ok.')
                    putText(crop_image, 10, 70, 'Front Save')   # 存檔
                else:
                    cv2.imwrite(os.path.join(self.save_path,
                                             f'photo-{self.shooted_num}.jpg'), crop_image_copy)
                    print(f'[INFO] {detect.t} : back image save ok.')
                    putText(crop_image, 10, 70, 'Back Save')   # 存檔

                if self.shooted_num == 2:
                    # 啟動detect
                    detect.run(source=self.save_path, project=os.path.join(self.save_path, 'detect'))
                    # Reset
                    self.reset()
                    self.get_detect_result()
                    self.is_detected = True # Pause for front end to show results

        # print(self.body,'xxx',self.a)
        _, jpeg = cv2.imencode('.jpg', crop_image)
        return jpeg.tobytes()
    
    def get_detect_result(self):
        folders = os.listdir('../photograph')
        save_path = os.path.join('../photograph', folders[-1])
        is_exist = os.path.exists(os.path.join(save_path, 'detect')) # 藉由第一個檔案來判定是否有正確辨識
        print(f'[DEBUG] Openning target folder: camera.save_path : {save_path} ; is_exist \'/detect\': {is_exist}')
        if is_exist:
            is_file_1_OK = True
            is_file_2_OK = True
            try:
                file_1 = open(os.path.join(save_path, 'detect', 'result1.txt'), 'r')
                result_1 = file_1.readlines()
                result_1_str = ' '.join(str(e) for e in result_1)
            except Exception as e:
                is_file_1_OK = False
                print(f"[ERROR] Unable to open file_1 \'{os.path.join(save_path, 'detect', 'result1.txt')}\': {e}")
            try:
                file_2 = open(os.path.join(save_path, 'detect', 'result2.txt'), 'r')
                result_2 = file_2.readlines()
                result_2_str = ' '.join(str(e) for e in result_2)
            except Exception as e:
                is_file_2_OK = False
                print(f"[ERROR] Unable to open file_1 \'{os.path.join(save_path, 'detect', 'result2.txt')}\': {e}")
            
            if is_file_1_OK and is_file_2_OK: 
                self.detected_result = f"正面:\n{result_1_str}\n背面:\n{result_2_str}".replace('\n', '<br>')
            elif is_file_1_OK:
                self.detected_result = f"正面:\n{result_1_str}\n".replace('\n', '<br>')
            elif is_file_2_OK:
                self.detected_result = f"背面:\n{result_2_str}\n".replace('\n', '<br>')
            else:
                self.detected_result = f"檢測失敗，查無檢測結果資料。"
