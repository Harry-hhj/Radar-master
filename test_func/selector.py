import cv2

ROI_name = ["偷家", "警戒区域", "能量机关", "我方打福定点", "敌方打福定点", "碉堡", "敌方基地", "敌方哨兵"]


def init(frame):
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
