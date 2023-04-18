import pyodbc


server = "DESKTOP-O6UFVI0"
database = 'PROJECT_PC01'
username = 'Project01'
password = 'Proyect01'

cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';ENCRYPT=yes'
                                                                                              ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()
print("conexión exitosa")


