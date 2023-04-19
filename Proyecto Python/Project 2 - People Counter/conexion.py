import pyodbc
import timeit

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-O6UFVI0;DATABASE=PROJECT_PC01;UID=sa;PWD=#projectPC')
cursor = conn.cursor()

# ahora un query basico
cursor.execute("SELECT * FROM conteo ")
for row in cursor.fetchall():
    print(row)

tiempo = timeit.timeit('lista = [i for i in range(1000000) if i%2==0]', number=5)
# Calculamos el tiempo medio
print(tiempo/5) # 0.18671