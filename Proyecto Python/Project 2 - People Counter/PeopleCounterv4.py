from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

cap = cv2.VideoCapture(0)

model = YOLO("../Yolo-Weights/yolov8n.pt")


classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush" ]


conteo = []
prev_frame_time = 0
new_frame_time = 0
count = 0

limitsUp = [103, 161, 296, 161]
trackers = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

while True:
    ret, frame = cap.read()
    # La region que captura
    # imgRegion  = cv2.bitwise_and(img)

    # Captura el frame que devuelve la camara
    results = model(frame, stream=True)

    detections = np.empty((0, 5))

    for r in results:

        # Dibujar recuadro del objeto

        boxes = r.boxes
        for box in boxes:
            # parametros del recuadro
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0]*100)) / 100
            cls = int(box.cls[0])

            # captura los nombres de las clases
            currentClass = classNames[cls]

            # compara los nombres de las clases con el objeto capturado
            # si objeto capturado = persona dibuja un recuadro al rededor
            if currentClass == "person" and conf > 0.3:
                # cornerRect dibuja el cuadro con los parámetros
                cvzone.cornerRect(frame, (x1, y1, w, h))

                # Coloca el nombre del objetos
                cvzone.putTextRect(frame, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultsTracker = trackers.update(detections)

    # Dibuja una linea límite
    cv2.line(frame, (limitsUp[0], limitsUp[1]),(limitsUp[2],limitsUp[3]), (0, 0, 255), 5)

    for results in resultsTracker:
        # Parametros para el contador
        x1, y1, x2, y2, id = results
        x1, y1, x2, y2 = int(x1), int(x1), int(x2), int(y2)
        print(id)

        w, h = x2 - x1, y2 - y1

        cx, cy = x1 + w // 2, y1 + h // 2
        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # si la persona pasa la linea límite se suma al contador
        if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[1] + 15:
            if conteo.count(id) == 0:
                conteo.append(id)
                cv2.line(frame, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 255, 0), 5)

    cv2.putText(frame, str(len(conteo)), (929, 345), cv2.FONT_HERSHEY_PLAIN, 5, (139, 195, 75), 7)

    cv2.imshow("Image", frame)
    cv2.waitKey(10)




