import sys
import os
from cx_freeze import setup, Executable

files = ['ContadorCTP.py', 'conexion.py','Fondo.png','requierements.txt']

exe = Executable(script="app.py", base="Win64GUI")

setup(
    name= "Contadod de Personas | Tiendas Cortitelas",
    version="0.1",
    author="Tania Villanueva",
    options={'build_exe': {'include_files': files}},
    executables=[exe]
)
