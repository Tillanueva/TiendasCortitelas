from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

cap = cv2.VideoCapture(0)

model = YOLO("../Yolo-Weights/yolov8l.pt")


classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
prev_frame_time = 0
new_frame_time = 0

trackers = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

while True:
    ret, frame = cap.read()
    #La region que captura
    #imgRegion  = cv2.bitwise_and(img)

    results = model(frame, stream=True)

    for r in results:

        # Dibujar recuadro del objetp
        boxes = r.boxes
        for box in boxes:
            # parametros del recuadro
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0]*100)) / 100
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "person" and conf > 0.3:
                # cornerRect dibuja el cuadro con los parámetros
                cvzone.cornerRect(frame, (x1, y1, w, h))
                cvzone.putTextRect(frame, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

  #  fps = 1 / (new_frame_time - prev_frame_time)
  #  prev_frame_time = new_frame_time
  #  print(fps)

    cv2.imshow("Image", frame)
    cv2.waitKey(1)




