import threading
import pid
import PWMServo
import math as m
from candidate import *
from config import *
from face_detect_yolo import *
from Motor import PWM_Motor
from kinematic import *

servo1_face_track = 1200
servo2_face_track = 1500
motor_face_track  = 1500
dis_ok_face = False
action_finish_face = True

servo1_pid3 = pid.PID(P=1.0, I=0.5, D=0.01)
servo2_pid4 = pid.PID(P=0.8, I=0.5, D=0.01)
motor_pid= pid.PID(P=1.0, I=0.5, D=0.01)   #待调节
motor=PWM_Motor(19)  #初始化机器人电机

def leMap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def track():
    global servo1_face_track, servo2_face_track
    global dis_ok_face, action_finish_face
    global motor, motor_face_track

    while True:
    #跟踪动作线程
        if dis_ok_face:
            dis_ok_face = False
            action_finish_face = False
            PWMServo.setServo(1, servo1_face_track, 20)
            PWMServo.setServo(2, servo2_face_track, 20)
            motor.setSpeed(motor_face_track)  #设置机器人电机速度
            time.sleep(0.02)
            action_finish_face = True
        else:
            time.sleep(0.01)

track_thread=threading.Thread(target=track,daemon=True)
track_thread.start()

#更新电机和舵机的位置
def update():
    global face_finder,height,width
    global servo1_pid3,servo2_pid4,motor_pid
    global servo1_face_track,servo2_face_track
    img_center_y=int(height/2)
    img_center_x=int(width/2)
    while True:
        #前处理
        c=face_finder.get_top_candidate()
        center_y=c.get_center_y()
        center_x=c.get_center_x()
        theta1=leMap(servo1_face_track,500,2500,-m.pi/2,m.pi/2)
        theta2=leMap(servo2_face_track,500,2500,-m.pi/2,m.pi/2)  #这里需要实际确定一下舵机控制量和坐标系转角之间的关系
        k=calcKinematic(theta1=theta1,theta2=theta2)
        x_bias=k.calcFacePosition(center_x,center_y,c.get_width(),c.get_height())

        servo1_pid3.SetPoint = center_y if abs(img_center_y - center_y) < 20 else img_center_y
        servo1_pid3.update(center_y)
        tmp = int(servo1_face_track - servo1_pid3.output)
        tmp = tmp if tmp > 500 else 500
        servo1_face_track = tmp if tmp < 2500 else 2500

        servo2_pid4.SetPoint = center_x if abs(img_center_x - center_x) < 40 else img_center_x
        servo2_pid4.update(2 * img_center_x - center_x)
        tmp = int(servo2_face_track + servo2_pid4.output)
        tmp = tmp if tmp > 500 else 500
        servo2_face_track = tmp if tmp < 2500 else 2500 #舵机角度限位

        #根据人脸偏移中心程度设置电机速度
        motor_pid.SetPoint = x_bias if abs(x_bias) < 80 else 0  #这里临界量待调节
        motor_pid.update(x_bias)
        tmp = int(1500 + motor_pid.output) if tmp > 2000 else 2000
        motor_face_track = tmp if tmp < 1000 else 1000


update_thread=threading.Thread(target=update,daemon=True)
update_thread.start()






