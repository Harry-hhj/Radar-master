import cv2
import threading
from pydarknet import Image
from const import const
from others.math import solve_coincide

test_state = const.test_state
SCORE = const.SCORE
COINCIDENCE = const.COINCIDENCE
ROI_name = const.ROI_name
ROI_name_trans = const.ROI_name_tans

test_state1 = False


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, net, frame, alarm_loc, detect_color):
        a: list
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.net = net
        self.frame = frame
        self.alarm_loc = alarm_loc
        self.detect_color = detect_color

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        if test_state and test_state1:
            print("Starting " + self.name)

        detect(self.net, self.frame, self.alarm_loc, self.detect_color)


def detect(net, frame, arr: list, enermy_color):
    dark_frame = Image(frame)
    results = net.detect(dark_frame)
    del dark_frame

    armor_friend = []
    armor_enermy = []
    armor_none = []
    car = []
    for cat, score, bounds in results:
        if score < SCORE:
            continue
        cls = str(cat.decode("utf-8"))
        if 'armor' in cls:
            if enermy_color in cls:
                armor_enermy.append((cat, score, bounds))
            elif 'grey' in cls:
                armor_none.append((cat, score, bounds))
            else:
                armor_friend.append((cat, score, bounds))
        elif 'car' in cls:
            car.append((cat, score, bounds))
        elif 'watcher' in cls:
            pass
        x, y, w, h = bounds
        cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0))
        cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

    text_pos = 20
    for i in range(len(arr)):
        cv2.rectangle(frame, (arr[i][0], arr[i][1]), (arr[i][0] + arr[i][2], arr[i][1] + arr[i][3]), (255, 0, 0))
        # print((arr[i][0], arr[i][1], arr[i][2], arr[i][3]), (int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)))
        for j in range(len(car)):
            x, y, w, h = car[j][2]
            a = solve_coincide((arr[i][0], arr[i][1], arr[i][0] + arr[i][2], arr[i][1] + arr[i][3]),
                               (int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)))
            # print(a)
            if a >= COINCIDENCE:
                flag = True
                for k in range(len(armor_enermy)):
                    x1, y1, w1, h1 = armor_enermy[k][2]
                    if int(x - w / 2) <= int(x1) <= int(x + w / 2) and int(y - h / 2) <= int(y1) <= int(y + h / 2):
                        cv2.putText(frame, "%s: detected enermy %s." % (
                            str(ROI_name_trans[arr[i][4]]), str(armor_enermy[k][0].decode("utf-8"))), (100, text_pos),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                        text_pos = text_pos + 30
                        flag = False
                        break
                for k in range(len(armor_friend)):
                    x1, y1, w1, h1 = armor_friend[k][2]
                    if int(x - w / 2) <= int(x1) <= int(x + w / 2) and int(y - h / 2) <= int(y1) <= int(y + h / 2):
                        flag = False
                        break
                if flag:
                    cv2.putText(frame, str(ROI_name_trans[arr[i][4]]) + ": Car not matched with armor.", (100, text_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                    text_pos = text_pos + 30
