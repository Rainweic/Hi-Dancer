import cv2

video = "/home/rainweic/test.mp4"

cap = cv2.VideoCapture(video)

cap.set(cv2.CAP_PROP_POS_MSEC, 10)
ret, frame = cap.read()
print(frame)