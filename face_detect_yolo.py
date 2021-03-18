import cv2
import numpy as np
import time
import sys
import os
import threading
from candidate import *
from yolo_handler import *
from config_yolo import *

#初始化yolo检测器
yolo_detector=YoloHandlerNCS2(config_dict,model_path)

#初始化找脸类对象
face_finder=YoloFaceDetector(config_dict,yolo_detector)

#开启摄像头
cap=cv2.VideoCapture(0)
count=0
while True:
    if cap.isOpened()==True:
        print("camera opened successfully")
        break
    else:
        print("camera open error!")
        count=count+1
        time.sleep(0.01)
        #cap.release()
        cap=cv2.VideoCapture(-1)

    if count>=6:
        print("camera cannot open,please check the device")
        sys.exit()

_,frame1=cap.read()
height,width=frame1.shape[:2]

def face_detect():
    #定义计数变量，用于异常退出
    count_exit=0
    #读取图片
    while True:
        ret,frame=cap.read()
        if ret==True:
            frame=cv2.flip(frame,0)
            face_finder.set_image(frame)
            face_finder.compute()
            if debug_face==True:
                frame_face=face_finder.draw_candidates()
                cv2.imshow("debug_face",frame_face)
                if cv2.waitKey(10)<0:
                    continue
        else:
            count_exit=count_exit+1
            print("cannot read image from camera!")
            try:
                cap.release()
            except Exception as e:
                print(e)
            cap=cv2.VideoCapture(-1)
            time.sleep(0.01)
        if count_exit>=5:
            os._exit()

face_detect_thread=threading.Thread(target=face_detect,daemon=True)
face_detect_thread.start()






