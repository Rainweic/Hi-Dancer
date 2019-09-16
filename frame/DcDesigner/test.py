import cv2

video = "~/test.mp4"

cap = cv2.VideoCapture(video)

cap.set(CV_CAP_PROP_POS_MSEC, 100)