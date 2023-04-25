import tkinter
from tkinter import *
import cv2
from PIL import Image, ImageTk
from sort import *
from datetime import *
from tkinter import messagebox
from Visualizar import PeopleCounter

InicioCam = PeopleCounter()


def iniciar():
    # Mostramos en el GUI
    lblVideo.configure(image=InicioCam)
    lblVideo.image = img
    lblVideo.after(5, visualizar)
    btnGuardar["state"] = tkinter.NORMAL
    InicioCam.visualizar()


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
