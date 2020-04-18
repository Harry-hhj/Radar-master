import cv2

cap = cv2.VideoCapture('../out.avi')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)&0xff
    if k == ord('1'):
        break

cap.release()
exit(1)
