#!/usr/bin/python
# -*- coding: UTF-8 -*-

# radar
from function import *
from pydarknet import Detector
import cv2
import time
import enum


class STATE(enum.Enum):
    TRACK = 0
    DETECT = 1
    MIX = 2


mode = STATE.DETECT  # mode.name  mode.value
print("''''''''''''''''''''''''''''''''''''''\nCurrent State is %s\n''''''''''''''''''''''''''''''''''''''" % mode.name)

'''''''''
要要调参的部分
'''''''''
test_state = True  ##
SCORE: float = 0.8
COINCIDENCE: float = 0.8
ROI_name = ["偷家", "警戒区域", "能量机关", "我方打福定点", "敌方打福定点", "碉堡", "敌方基地", "敌方哨兵"]


enermy_color: str = 'blue'
show_image: str = 'down'
net1 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
net2 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))


def getVarable(v: tuple):
    tmp = []
    for i in v:
        if v[i] in locals().keys():
            tmp.append(eval(v[i]))
        else:
            print('no')
            input("Press Ctrl-C to STOP and check file<function.py>")
    return


def init(framedown, frameup):
    enermy_color = input("Please input enermy_color: ('r' for red and 'b' for blue)\n")
    if enermy_color[0] == 'r':
        enermy_color = 'red'
    elif enermy_color[0] == 'b':
        enermy_color = 'blue'
    else:
        enermy_color = input("Incorrect input, please input again: ('r' for red and 'b' for blue)\n")
        if enermy_color[0] == 'r':
            enermy_color = 'red'
        elif enermy_color[0] == 'b':
            enermy_color = 'blue'

    alarm_loc_down = ROI_init(framedown)
    alarm_loc_up = ROI_init(frameup)

    return enermy_color, alarm_loc_down, alarm_loc_up





if __name__ == "__main__":

    # 机机初始化
    frame1 = None
    frame2 = None
    cap1 = cv2.VideoCapture("test_data/1.mp4")
    cap2 = cv2.VideoCapture("test_data/2.MOV")
    r1, frame1 = cap1.read()
    r2, frame2 = cap2.read()
    if not r1 or not r2:
        print("Someting go wrong with the camera......")

    enermy_color, alarm_loc_down, alarm_loc_up = init(frame1, frame2)

    cv2.destroyAllWindows()
    cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
    counter = 0
    while True:
        start_time = time.time()
        # 取图片
        r1, frame1 = cap1.read()
        r2, frame2 = cap2.read()

        if not r1 or not r2:
            print("Someting go wrong with the camera......")
            continue
        if mode.value:
            thread1 = myThread(1, "Thread-1", net1, frame1, alarm_loc_down, enermy_color)
            thread1.start()
            thread2 = myThread(2, "Thread-2", net2, frame2, alarm_loc_up, enermy_color)
            thread2.start()
            threads = []
            for i in range(3):
                if i == 0:
                    continue
                threads.append(eval("thread" + str(i)))
            for t in threads:
                t.join()
            else:
                pass
        if test_state:
            print('Time consumed: ', time.time() - start_time)

        if show_image == 'up':
            cv2.imshow("Show", frame2)
        else:
            cv2.imshow("Show", frame1)
        k = cv2.waitKey(1)
        if k == 0xFF & ord("q") and test_state:
            break
        elif k == 0xFF & ord("a") and test_state:
            if show_image == 'down':
                show_image = 'up'
            else:
                show_image = 'down'
