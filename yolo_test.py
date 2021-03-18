import cv2
import numpy as np
from candidate import *
from yolo_handler import *
from config_yolo import *

cap=cv2.VideoCapture(0)

yolo_model=YoloHandlerNCS2(config_dict,model_path)
yolo_face_detector=YoloFaceDetector(config_dict,yolo_model)

while True:
    ret,frame=cap.read()
    if ret==True:
        yolo_face_detector.set_image(frame)
        yolo_face_detector.compute()
        face_frame=yolo_face_detector.draw_candidates()
        cv2.imshow('face',face_frame)
        if cv2.waitKey(50)>0:
            break


cap.release()
cv2.destroyAllWindows()
