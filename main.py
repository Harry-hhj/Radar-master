#!/usr/bin/python
# -*- coding: UTF-8 -*-

# radar
from pydarknet import Detector
import cv2, time, enum
from others.ROI import ROI_init
from others.math import solve_coincide
from detect.learning import myThread, detect
from detect.frame_difference import diffdetect
from const import const
from detect.message.warning import warningMessage
from camera.camera import Camera


class STATE(enum.Enum):
    TRACK = 0
    DETECT = 1
    DETECT_DIFF = 2
    MIX = 3


''''''''''''''''''''''''''''''''''''''''
调参数请前往const包
'''''''''''''''''''''''''''''''''''''''''
mode = STATE.DETECT  # mode.name  mode.value
print('\''*50)
print("Current State is ")
print('\''*50)
print(mode.name)

source = 0  # 0:Video 1:Camera

test_state = const.test_state
record_state = const.record_state
main_cam_num = const.main_cam_num
SCORE = const.SCORE
COINCIDENCE = const.COINCIDENCE
ROI_name = const.ROI_name
ROI_name_tans = const.ROI_name_tans

enermy_color = const.enermy_color
show_image = const.show_image


def init(framedown, frameup=None):
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

    if frameup is not None:
        alarm_loc_down = ROI_init(framedown)
        alarm_loc_up = ROI_init(frameup)

        return enermy_color, alarm_loc_down, alarm_loc_up
    else:
        alarm_loc = ROI_init(framedown)
        return enermy_color, alarm_loc


if __name__ == "__main__":
    # writer = cv2.VideoWriter("out2.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), 20.0, (1000, 600))
    if mode.name != 'DETECT_DIFF':
        net1 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0, bytes("cfg/coco.data", encoding="utf-8"))
        net2 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0, bytes("cfg/coco.data", encoding="utf-8"))

    if main_cam_num == 2:
        # 机机初始化
        if source == 0:
            cap1 = cv2.VideoCapture("test_data/t1.mov")
            cap2 = cv2.VideoCapture("test_data/2.MOV")
        elif source == 1:
            cap1 = Camera()
            cap2 = Camera()
        r1, frame1 = cap1.read()
        r2, frame2 = cap2.read()
        if not r1 or not r2:
            RuntimeError("Someting go wrong with the camera......")
            exit(404)
        enermy_color, alarm_loc_down, alarm_loc_up = init(frame1, frame2)

        cv2.destroyAllWindows()
        cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
        counter = 0
        a = warningMessage()
        b = warningMessage()
        while True:
            start_time = time.time()
            # 取图片s
            frame_1 = frame1
            frame_2 = frame2
            r1, frame1 = cap1.read()
            r2, frame2 = cap2.read()

            if not r1 or not r2:
                RuntimeError("Someting go wrong with the camera......")
                continue
            if mode.name == 'DETECT':
                thread1 = myThread(1, "Thread-1", net1, frame1, alarm_loc_down, enermy_color, a)
                thread1.start()
                a.show()
                thread2 = myThread(2, "Thread-2", net2, frame2, alarm_loc_up, enermy_color, b)
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

                if show_image == 'up':
                    cv2.imshow("Show", frame2)
                else:
                    cv2.imshow("Show", frame1)
            elif mode.name == 'DETECT_DIFF':
                frame1_draw = diffdetect(frame_1, frame1, alarm_loc_down, enermy_color)
                frame2_draw = diffdetect(frame_2, frame2, alarm_loc_up, enermy_color)
                if show_image == 'up':
                    cv2.imshow("Show", frame2_draw)
                else:
                    cv2.imshow("Show", frame1_draw)
                farme_1 = frame1
                frame_2 = frame_2

            if test_state:
                print('Time consumed: ', time.time() - start_time)

            k = cv2.waitKey(1)
            if k == 0xFF & ord("q") and test_state:
                break
            elif k == 0xFF & ord("a") and test_state:
                if show_image == 'down':
                    show_image = 'up'
                else:
                    show_image = 'down'
            cv2.waitKey(1)

    elif main_cam_num == 1:
        # 机机初始化
        if source == 0:
            cap1 = cv2.VideoCapture("test_data/t1.mov")
        elif source == 1:
            cap1 = Camera()
        r1, frame1 = cap1.read()
        if not r1:
            print("Someting go wrong with the camera......")

        enermy_color, alarm_loc = init(frame1)

        cv2.destroyAllWindows()
        cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
        counter = 0
        while True:
            start_time = time.time()
            # 取图片
            frame_1 = frame1
            r1, frame1 = cap1.read()

            if not r1:
                print("Someting go wrong with the camera......")
                continue
            if mode.name == 'DETECT':
                detect(net1, frame1, alarm_loc, enermy_color)
                cv2.imshow("Show", frame1)
                # frame1 = cv2.resize(frame1, (1000,600))
                # writer.write(frame1)
            else:
                frame = diffdetect(frame_1, frame1, alarm_loc, enermy_color)
                frame_1 = frame1
                cv2.imshow("Show", frame)
            if test_state:
                print('Time consumed: ', time.time() - start_time)

            k = cv2.waitKey(100)
            if k == 0xFF & ord("q") and test_state:
                break
