import os
import sys
import pyodbc
from conexion import conex

# CONEXION BASE DE DATOS
conn = conex.connec
cursor = conn.cursor()

cursor.execute(" exec ConeoDiarioDesc")
records = []
records = cursor.fetchall()

count = 0
for i in records:
    traficoDiario = {
        i[0]: i[1]
    }
    # print(traficoDiario)

cursor.execute(" exec ConteoMesDesc")
records = []
records1 = cursor.fetchall()

trafMens = {
    records1[0]:records1[1]
}

print(mes.trafMens)
