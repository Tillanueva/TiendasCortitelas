import pyodbc

server = "DESKTOP-O6UFVI0"
bd = 'PeopleCounter'
user = 'admin'
password = 'Proyect01'

try:
    cn = pyodbc.connect(
        'DRIVER = {ODBC Driver 17 for SQL server};SERVER=' + server + ';DATABASE=' + bd + ';UID=' + user + ';PWD=' + password
    )
    print("conexión exitosa")
except:
    print("Error al intentar conectarse")
