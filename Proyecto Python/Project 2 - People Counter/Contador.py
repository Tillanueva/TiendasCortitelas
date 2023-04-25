import tkinter

import cv2
import math
import cvzone
from ultralytics import YOLO
from tkinter import *
from PIL import Image, ImageTk
from sort import *
from datetime import *
import pyodbc
import timeit
from tkinter import messagebox

# CONEXION BASE DE DATOS
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-O6UFVI0;DATABASE=PROJECT_PC01;UID=sa;PWD=#projectPC')

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
global count
# Coordenadas límites verticales para poder contar a la persona
limitsUp = [0, 300, 1280, 300]  # Entrada

# variable de seguimiento de objetos
trackers = Sort(max_age=20, min_hits=3, iou_threshold=0.3)


def visualizar():

    if cap is not None:

        ret, frame = cap.read()

        if ret:

            if rgb == 1 and hsv == 0 and gray == 0:
                # Color BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            elif rgb == 0 and hsv == 1 and gray == 0:
                # Color HSV
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            elif rgb == 0 and hsv == 0 and gray == 1:
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

                    # Si el objeto es una persona, dibuja un recuadro alrededor
                    if classNames[cls] == "person" and conf > 0.3:
                        # cornerRect dibuja el cuadro con los parámetros anteriores
                        cvzone.cornerRect(frame, (x1, y1, w, h))

                        # Coloca el nombre del objeto (persona)
                        cvzone.putTextRect(frame, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1,
                                           thickness=1)

                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))
            # Actualiza en tiempo real lo que captura el video
            resultsTracker = trackers.update(detections)

            for results in resultsTracker:
                # Parametros para el contador
                x1, y1, x2, y2, id1 = results
                x1, y1, x2, y2 = int(x1), int(x1), int(x2), int(y2)

                w, h = x2 - x1, y2 - y1
                # Ecuación de definición de punto medio
                cx, cy = x1 + w // 2, y1 + h // 2

                # Dibuja un punto medio en el recuadro de la persona
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # si la persona pasa la linea límite se suma al contador de personas que entran
                if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[1] + 15:
                    if conteo.count(id1) == 0:
                        conteo.append(id1)
                        cv2.line(frame, (limitsUp[3], limitsUp[2]), (limitsUp[1], limitsUp[0]), (0, 255, 0), 5)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(5, visualizar)

            # Muestra en conteo de personas en la ventana
            global count
            count = str(len(conteo))
            lblConteo = Label(pantalla, text="Ingreso de personas: " + count)
            lblConteo.config(font="Sans-serif")
            lblConteo.place(x=660, y=10)
            return count

        else:

            cap.release()


def iniciar():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, 1500)
    cap.set(4, 520)
    btnGuardar["state"] = tkinter.NORMAL
    visualizar()


def finalizar():
    cap.release()
    cv2.destroyAllWindows()
    print("FIN")


def guardar():
    cursor = conn.cursor()
    consulta = "INSERT INTO conteo(entradas) VALUES (?);"
    try:
        with cursor:
            cursor.execute(consulta, visualizar())
            messagebox.showinfo(title="Guardado", message="Guardado Exitosamente")
    except Exception as e:
        print("Ocurrió un error al insertar: ", e)
        messagebox.showerror(title="Error", message="Ocurrió un error al guardar")


def times():
    fechaC = datetime.today()  # Capruta date actual
    current_date = fechaC.strftime("%m/%d/%Y")
    lblFecha.config(text=current_date, font="Sans-serif")


# VARIABLES
cap = None
rgb = 1
hsv = 0
gray = 0

# INTERFAZ
pantalla = Tk()
pantalla.title("Tiendas Cortitelas | People Counter")
pantalla.geometry("880x580")  # Dimensión de la ventana

# Fondo
imagenF = PhotoImage(file="Fondo.png")
background = Label(image=imagenF, text="Fondo")
background.place(x=0, y=0, relwidth=1, relheight=1)

texto1 = Label(pantalla, text="Video en tiempo real: ")
texto1.config(font="Sans-serif")
texto1.place(x=300, y=10)

# Muestra fecha actual
lblFecha = Label(pantalla)
lblFecha.place(x=10, y=10)
times()  # Función captura fecha actual

# BOTONES
# Iniciar
imgInicio = PhotoImage(file="Inicio.png")
inicio = Button(pantalla, text="Iniciar", image=imgInicio, height="40", width="200", command=iniciar)
inicio.place(x=660, y=80)

# Guardar
imgGuardar = PhotoImage(file="guardar.png")
btnGuardar = Button(pantalla, text="Guardar", image=imgGuardar, height="40", width="200", command=guardar,
                    state=tkinter.DISABLED)
btnGuardar.place(x=660, y=140)

# Video
lblVideo = Label(pantalla)
lblVideo.place(x=10, y=60)

pantalla.mainloop()
