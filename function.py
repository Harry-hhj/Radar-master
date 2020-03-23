import cv2
import threading
from pydarknet import Image


test_state = True  ##
SCORE: float = 0.8
COINCIDENCE: float = 0.8
ROI_name = ["偷家", "警戒区域", "能量机关", "我方打福定点", "敌方打福定点", "碉堡", "敌方基地", "敌方哨兵"]


def ROI_init(frame):
    arr = []
    # frame = cv2.imread("map.jpg")
    # frame = cv2.resize(frame, (1280, 960))
    ROI_message = "Input type here:("
    for i in range(len(ROI_name)):
        ROI_message = ROI_message + str(i) + ":" + ROI_name[i] + "，"
    ROI_message = ROI_message + "C:取消)"

    while True:
        bbox = []
        tmp = cv2.selectROI(frame, False)
        ROI_type = -1
        ROI_type = input(ROI_message + "\n")  # +判断函数
        if ROI_type == 'c' or ROI_type == 'C':
            break
        for i in range(4):
            bbox.append(tmp[i])
        bbox.append(int(ROI_type))
        arr.append(bbox)

#    print(bbox)
#    print('\n')
#    print(arr)
    return arr


def mat_inter(box1, box2):
    x01, y01, x02, y02 = box1
    x11, y11, x12, y12 = box2

    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False


def solve_coincide(box1, box2):
    if mat_inter(box1, box2) == True:
        x01, y01, x02, y02 = box1
        x11, y11, x12, y12 = box2
        col = min(x02, x12) - max(x01, x11)
        row = min(y02, y12) - max(y01, y11)
        intersection = col * row
        area1 = (x02 - x01) * (y02 - y01)
        area2 = (x12 - x11) * (y12 - y11)
        coincide = intersection / area2
        return coincide
    else:
        return False


class backup:
    def __init__(self):
        self.bakg_up = None
        self.bakg_down = None

    def copy_bakg(self, frame1, frame2):
        self.bakg_down = frame1
        self.bakg_up = frame2

    def check_bakg(self, index: str = 'down'):
        return self.bakg_down if index == 'down' else self.bakg_up


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
        if test_state:
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
                        cv2.putText(frame, "%s detected enermy %s." % (
                            str(ROI_name[i]), str(armor_enermy[k][0].decode("utf-8"))), (100, text_pos),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                        text_pos = text_pos + 30
                        flag = False
                        break
                if flag:
                    cv2.putText(frame, str(ROI_name[i]) + ": Car not matched with armor.", (100, text_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                    text_pos = text_pos + 30
                    print("Car not matched with armor.")
