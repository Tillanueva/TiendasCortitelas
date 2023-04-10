import cv2
import imutils
import math
import cvzone
import numpy as np
from ultralytics import YOLO
from tkinter import *
from PIL import Image, ImageTk
from sort import *
from datetime import *

# inicializar el Modelo de YOLOY
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
              "teddy bear", "hair drier", "toothbrush"]

# Variables de conteo
conteo = []
salidas = []

# Coordenadas límites verticales para poder contar a la persona
limitsUp = [0, 300, 1280, 300]               # Entrada
limitsDown = [0, 400, 1280, 400]             # salida

# variable de seguimiento de objetos
trackers = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

def visualizar():
    if cap is not None:

        ret, frame = cap.read()

        if ret == True:

            if (rgb == 1 and hsv == 0 and gray == 0):
                # Color BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            elif rgb == 0 and hsv == 1 and gray == 0:
                # Color HSV
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            elif (rgb == 0 and hsv == 0 and gray == 1):
                # Color GRAY
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # captura el modelo del frame que capturó la cámara web y la lee en tiempo real
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

                    # la variable cls captura los distintos objetos que se encuentran alrededor
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    print(cls)

                    # Si el objeto es una persona, dibuja un recuadro alrededor
                    if classNames[cls] == "person" and conf > 0.3:
                        # cornerRect dibuja el cuadro con los parámetros anteriores
                        cvzone.cornerRect(frame, (x1, y1, w, h))

                        # Coloca el nombre del objetos
                        cvzone.putTextRect(frame, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1,
                                           thickness=1)

                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))

            resultsTracker = trackers.update(detections)

            # Dibuja una linea límite (donde está ubicada la linea del contador) (Prueba)
            # cv2.line(frame, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 0, 255), 5)
            # cv2.line(frame, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 0, 255), 5)

            for results in resultsTracker:
                # Parametros para el contador
                x1, y1, x2, y2, id = results
                x1, y1, x2, y2 = int(x1), int(x1), int(x2), int(y2)
                print(id)

                w, h = x2 - x1, y2 - y1

                cx, cy = x1 + w // 2, y1 + h // 2

                # Dibuja un punto central en el recuadro de la persona
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # si la persona pasa la linea límite se suma al contador de personas que entran
                if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[1] + 15:
                    if conteo.count(id) == 0:
                        conteo.append(id)
                        cv2.line(frame, (limitsUp[3], limitsUp[2]), (limitsUp[1], limitsUp[0]), (0, 255, 0), 5)
                # si la persona pasa la linea límite se suma al contador de personas que salen
                if limitsDown[0] < cx < limitsDown[2] and limitsDown[1] - 15 < cy < limitsDown[1] + 15:
                    if salidas.count(id) == 0:
                        salidas.append(id)
                        cv2.line(frame, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 255, 0), 5)

            # Imprime el conteo de personas
            cv2.putText(frame, str(len(conteo)), (895, 115), cv2.FONT_HERSHEY_PLAIN, 5, (139, 195, 75), 7)
            cv2.putText(frame, str(len(salidas)), (1150, 115), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 230), 7)

            print(conteo)
            print(salidas)

            frame = imutils.resize(frame)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)

        else:
            cap.release()


def iniciar():
    global cap
    # Inicialización de cámara
    cap = cv2.VideoCapture(0)
    cap.set(3, 1200)
    cap.set(4, 520)

    visualizar()


def finalizar():
    cap.release()
    cv2.DestroyAllWindows()
    print("FIN")

def times():
    time = datetime.today()
    current_date = time.strftime("%m/%d/%Y")
    lblFecha.config(text=current_date)

# VARIABLES
cap = None
rgb = 1
hsv = 0
gray = 0


# INTERFAZ
pantalla = Tk()
pantalla.title("Tiendas Cortitelas | People Counter")
pantalla.geometry("1280x720")  # Dimensión de la ventana

# Fondo
imagenF = PhotoImage(file="Fondo.png")
background = Label(image=imagenF, text="Fondo")
background.place(x=0, y=0, relwidth= 1, relheight=1)

texto1 = Label(pantalla, text="VIDEO EN TIEMPO REAL: ")
texto1.place(x = 580, y = 10)

lblFecha = Label(pantalla)
lblFecha.place(x=10, y=10)
times()

# CONTEO
imgConteo = PhotoImage(file="graphics.png")
lblConteo = Label(image=imgConteo)
lblConteo.place(x=1000, y=50)
# BOTONES
# Iniciar
imgInicio = PhotoImage(file = "Inicio.png")
inicio = Button(pantalla, text="Iniciar", image=imgInicio, height="40", width="200", command=iniciar)
inicio.place(x=90, y=600)

#Finalizar video
imgFinalizar = PhotoImage(file="Finalizar.png")
final = Button(pantalla, text="Finalizar", image=imgFinalizar, height="40", width="200", command=finalizar)
final.place(x=1000, y=600)


# Video
lblVideo = Label(pantalla)
lblVideo.place(x=165, y=50)

lblVideo2 = Label(pantalla)
lblVideo2.place(x=470, y=500)

pantalla.mainloop()