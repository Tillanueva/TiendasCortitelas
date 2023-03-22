import cv2
import numpy as np
from sort import Sort



# Inicializar el objeto de seguimiento SORT
tracker = Sort()

# Inicializar el clasificador de detección de objetos de OpenCV
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Inicializar las variables de seguimiento de objetos
trackers = []
track_ids = []
deleted_tracks = []


# Inicializar la variable de recuento de personas
people_count = 0

# Inicializar la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Capturar un fotograma de la cámara web
    ret, frame = cap.read()

    # Detectar objetos en el fotograma actual, develve 0
    # bbox no lee ningún fotograma
    bbox = hog.detectMultiScale(frame)
    print(bbox)

    # Actualizar los objetos detectados con el seguimiento SORT
    detections = np.array([[x, y, x+w, y+h] for x,y,w,h in bbox], dtype=np.float32)
    trackers = tracker.update(detections)
    track_ids = [int(x) for x in trackers[:,4]]

    # Contar las personas detectadas en el fotograma actual
    current_people_count = len(track_ids)

    # Filtrar los objetos detectados que han sido eliminados por el seguimiento
    for id in deleted_tracks:
        if id in track_ids:
            track_ids.remove(id)

    # Añadir las personas contadas en el fotograma actual al recuento total
    people_count += current_people_count - len(track_ids)

    # Dibujar los cuadros de seguimiento de los objetos detectados
    for bbox, track_id in zip(trackers[:,:4], track_ids):
        x1, y1, x2, y2 = [int(x) for x in bbox]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(track_id), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Mostrar el fotograma actual y el recuento total de personas
    cv2.imshow("Frame", frame)
    cv2.putText(frame, "People Count: {}".format(people_count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    key = cv2.waitKey(1)

    # Salir del bucle si se presiona la tecla "q"
    if key == ord("q"):
        break

    # Actualizar la lista de objetos eliminados
    deleted_tracks = [id for id in track_ids if id not in deleted_tracks]

# Liberar los recursos y
cap.release()
cv2.destroyAllWindows()
