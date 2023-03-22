import numpy as np
import cv2
import sys
from imutils.object_detection import non_max_suppression

cap = cv2.VideoCapture(0)
hog_descriptor = cv2.HOGDescriptor()
hog_descriptor.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

tracker = cv2.TrackerKCF_create()
ret, frame = cap.read()

while (1):
    ret, frame = cap.read()
    (rects, weights) = hog_descriptor.detectMultiScale(frame, winStride=(16, 16), padding=(8, 8), scale=1.05)


    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in rects:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    ret = tracker.init(frame)

    ret, = tracker.update(frame)
    cv2.imshow("video", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()