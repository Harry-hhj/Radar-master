#

import time
import numpy as np
import cv2
from armor.color_distinguish import get_color
from const import const
from others.ROI import ROI_init
from others.math import solve_coincide


test_state = const.test_state


def absdiff_demo(image_1, image_2, sThre):
    gray_image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)  # 灰度化
    gray_image_1 = cv2.GaussianBlur(gray_image_1, (5, 5), 0)  # 高斯滤波
    gray_image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
    gray_image_2 = cv2.GaussianBlur(gray_image_2, (5, 5), 0)
    d_frame = cv2.absdiff(gray_image_1, gray_image_2)
    ret, d_frame = cv2.threshold(d_frame, sThre, 255, cv2.THRESH_BINARY)
    return d_frame


def absdiff_check(position): ##
    if isinstance(position, list):
        print(position)
    else:
        RuntimeError("absdiff_check can only process list")


if __name__ == '__main__':
    capture = cv2.VideoCapture("test_data/11.mp4")
    sThre = 10  # sThre表示像素阈值
    i = 0
    ret, frame = capture.read()
    arr = ROI_init(frame)
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        if i == 0:
            cv2.waitKey(1)
            i = i + 1
        ret_2, frame_2 = capture.read()
        if not ret_2:
            break
        start = time.time()
        segMap = absdiff_demo(frame, frame_2, sThre)
        if time.time() - start > 0.01 and test_state:
            print("cost time", time.time() - start, frame.shape[:])
        if test_state:
            cv2.imshow("frame_difference:asdf", segMap)
        # cv2.waitKey(1)

        kernel = np.ones((4, 4), np.uint8)
        segMap = cv2.morphologyEx(segMap, cv2.MORPH_OPEN, kernel)

        kernel = np.ones((20, 20), np.uint8)
        segMap = cv2.morphologyEx(segMap, cv2.MORPH_CLOSE, kernel)
        kernel1 = np.ones((5, 5), np.uint8)
        segMap = cv2.dilate(segMap, kernel1, iterations=1)

        # binary, contours, hierarchy = cv2.findContours(segMap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 该函数计算一幅图像中目标的轮廓
        contours, hierarchy = cv2.findContours(segMap, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        rect = []
        if 0 < len(contours) < 10:
            for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)

                if w * h < 400:
                    continue
                rect.append((x, y, w, h))  # x代表横向
                for i in range(len(arr)):
                    if solve_coincide((arr[i][0], arr[i][1], arr[i][0] + arr[i][2], arr[i][1] + arr[i][3]),(x,y,x+w,y+h))>0.8:
                        print('matched')
                img = frame_2[y:y + h, x:x + w]
                print(get_color(img))
                cv2.rectangle(frame_2, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if test_state:
            cv2.imshow("frame_difference:res", frame_2)
            k = cv2.waitKey(500) & 0xff
            if k == ord('p'):
                cv2.waitKey(0)
            elif k == ord('q'):
                break

    cv2.destroyAllWindows()
    exit(1)

    # 相邻举着大小不同就何合并
