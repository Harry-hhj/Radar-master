#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
from pydarknet import Detector, Image
import cv2

exitFlag = 0
net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
               bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
               bytes("cfg/coco.data", encoding="utf-8"))
net1 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
net2 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
net3 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
'''''''''''
net4 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
net5 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
net6 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
net7 = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"),
                bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0,
                bytes("cfg/coco.data", encoding="utf-8"))
'''''''''
cap = cv2.VideoCapture("/home/radar/Desktop/Radar/testVideo.mp4")
r, frame = cap.read()
r1, frame1 = cap.read()
r2, frame2 = cap.read()
r3, frame3 = cap.read()
#r4, frame4 = cap.read()
#r5, frame5 = cap.read()
#r6, frame6 = cap.read()
#r7, frame7 = cap.read()
flag = [0,0,0,0]


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, net, frame):
        a: list
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.net = net
        self.frame = frame

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)

        average_time = 0

        if True:
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(self.frame)
            results = self.net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            average_time = average_time * 0.8 + (end_time - start_time) * 0.2
            # Frames per second can be calculated as 1 frame divided by time required to process 1 frame
            fps = 1 / (end_time - start_time)

            #print("FPS: ", fps)
            #print("Total Time:", end_time - start_time, ":", average_time)

            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0))
                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 0))

            cv2.imshow("preview", frame)
        print("Exiting " + self.name)


# 创建新线程
thread1 = myThread(1, "Thread-1", net, frame)
thread1.start()
thread2 = myThread(2, "Thread-2", net1, frame1)
thread2.start()
thread3 = myThread(3, "Thread-3", net2, frame2)
thread3.start()
thread4 = myThread(4, "Thread-4", net3, frame3)
thread4.start()

threads = []
for i in range(5):
    if i == 0:
        continue
    threads.append(eval("thread" + str(i)))

r, frame = cap.read()
r1, frame1 = cap.read()
r2, frame2 = cap.read()
r3, frame3 = cap.read()

while r and r1 and r2 and r3:
    t0 = time.time()

    r, frame = cap.read()
    thread1.join()
    thread1 = myThread(1, "Thread-1", net, frame)
    thread1.start()
    r1, frame1 = cap.read()
    thread2.join()
    thread2 = myThread(2, "Thread-2", net1, frame1)
    thread2.start()
    r2, frame2 = cap.read()
    thread3.join()
    thread3 = myThread(3, "Thread-3", net2, frame2)
    thread3.start()
    r3, frame3 = cap.read()
    thread4.join()
    thread4 = myThread(4, "Thread-4", net3, frame3)
    thread4.start()
    #thread5 = myThread(5, "Thread-5", net4, frame4)
    #thread6 = myThread(6, "Thread-6", net5, frame5)
    #thread7 = myThread(7, "Thread-7", net6, frame6)
    #thread8 = myThread(8, "Thread-8", net7, frame7)

    # 开启线程




    #thread5.start()
    #thread6.start()
    #thread7.start()
    #thread8.start()


    #for t in threads:
        #t.join()
    #print("Exiting Main Thread")
    print(time.time() - t0)
