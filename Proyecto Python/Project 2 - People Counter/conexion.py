import pyodbc

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-O6UFVI0;DATABASE=PROJECT_PC01;UID=sa;PWD=#projectPC')
cursor = conn.cursor()

# ahora un query basico
cursor.execute("SELECT * FROM conteo ")
for row in cursor.fetchall():
    print(row)
