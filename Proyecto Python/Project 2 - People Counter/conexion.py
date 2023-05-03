import pyodbc
import os


class conex:
    connec = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-O6UFVI0;DATABASE=PROJECT_PC01;UID=sa;PWD=#projectPC')
