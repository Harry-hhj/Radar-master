import time

from pydarknet import Detector, Image
import cv2
import selector

ARMOR_COLOR = 'red'  # wofangyanse
SCORE = 0.8
COINCIDENCE = 0.8
data_detected_path = "./data_detected.txt"
ROI_name = ["偷家", "警戒区域", "能量机关", "我方打福定点", "敌方打福定点", "碉堡", "敌方基地", "敌方哨兵"]

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

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process a video.')
    parser.add_argument('path', metavar='video_path', type=str,
                        help='Path to source video')

    args = parser.parse_args()
    print("Source Path:", args.path)
    cap = cv2.VideoCapture(args.path)


    average_time = 0

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3_130000.weights", encoding="utf-8"), 0, bytes("cfg/coco.data", encoding="utf-8"))

    arr = []
    r, frame = cap.read()
    if r:
        arr = selector.init(frame)
    print(len(arr))
    input()

    counter = 0
    while True:
        r, frame = cap.read()
        if r:
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            average_time = average_time * 0.8 + (end_time-start_time) * 0.2

            print("Total Time:", end_time-start_time, ":", average_time)

            armor_friend = []
            armor_enermy = []
            armor_none = []
            car = []
            for cat, score, bounds in results:
                if score < SCORE:
                    continue
                cls = str(cat.decode("utf-8"))
                if 'armor' in cls:
                    if ARMOR_COLOR in cls:
                        armor_friend.append((cat, score, bounds))
                    elif 'grey' in cls:
                        armor_none.append((cat, score, bounds))
                    else:
                        armor_enermy.append((cat, score, bounds))
                elif 'car' in cls:
                    car.append((cat, score, bounds))
                elif 'watcher' in cls:
                    pass
                x, y, w, h = bounds
                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

            text_pos = 20
            for i in range(len(arr)):
                # print((arr[i][0], arr[i][1], arr[i][2], arr[i][3]), (int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)))
                for j in range(len(car)):
                    x, y, w, h = car[j][2]
                    a = solve_coincide((arr[i][0], arr[i][1], arr[i][0] + arr[i][2], arr[i][1] + arr[i][3]), (int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)))
                    # print(a)
                    if a >= COINCIDENCE:
                        flag = True
                        for k in range(len(armor_enermy)):
                            x1, y1, w1, h1 = armor_enermy[k][2]
                            if int(x-w/2) <= int(x1) <= int(x+w/2) and int(y-h/2) <= int(y1) <= int(y+h/2):
                                cv2.putText(frame, "%s detected enermy %s." % (str(ROI_name[i]), str(armor_enermy[k][0].decode("utf-8"))), (100, text_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                                text_pos = text_pos + 30
                                flag = False
                                break
                        if flag:
                            cv2.putText(frame, "Car not matched with armor.", (100, text_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                            text_pos = text_pos + 30
                            print("Car not matched with armor.")

            cv2.imshow("preview", frame)
            counter += 1
            if time.time() - start_time:
                print("FPS: ", counter / (time.time() - start_time))
                counter = 0
                start_time = time.time()


        k = cv2.waitKey(1)
        if k == 0xFF & ord("q"):
            break

if __name__ == "__main__":
    main()
