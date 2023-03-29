import tkinter as tk
from functools import partial
from tkinter import messagebox, ttk

def saludar(ventana):
    messagebox.showinfo(message="¡Hola, mundo!", title="Saludo")
    ventana.title("Nuevo título")

root = tk.Tk()
root.config(width=300, height=200)
root.title("Botón en Tk")

boton = ttk.Button(text="¡Hola, mundo!", command=partial(saludar, root))
boton.place(x=50, y=50)

root.mainloop()