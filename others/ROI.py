import cv2
import re

from const.const import ROI_name


def ROI_init(frame):
    type_regex = r'^[0-9][0-9]?$'
    cv2.namedWindow('ROI_init', cv2.WINDOW_NORMAL)

    print('ROI initializing.....')
    print('='*50)

    frame_copy = frame.copy()
    loc = []
    # frame = cv2.resize(frame, (1280, 960))
    ROI_message = "Input type here:("
    for i in range(len(ROI_name)):
        ROI_message = ROI_message + str(i) + ":" + ROI_name[i] + "，"
    ROI_message = ROI_message + "C:取消)"

    while True:
        tmp = cv2.selectROI(frame, False)
        ROI_type = input(ROI_message + "\n")
        if ROI_type == 'c' or ROI_type == 'C':
            break
        if re.search(type_regex, ROI_type):
            bbox = []
            for i in range(4):
                bbox.append(tmp[i])
            bbox.append(int(ROI_type))
            loc.append(bbox)

            cv2.rectangle(frame_copy, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame_copy, ROI_type, (bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            cv2.imshow('ROI_init', frame_copy)
        else:
            print('Invalid input. Please try again. Notice this will not be add to list.')

    print('ROI finished.....')
    print('='*50)
    print(loc)

    return loc  # loc[i][0] 左上角横向 loc[i][1] 左上角纵向 loc[i][2] 横向宽度 loc[i][3] 纵向宽度
