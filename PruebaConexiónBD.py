#Conexion a base de datos
import mysql.connector
from datetime import datetime 

SERVER = "localhost"
USER = "BDpython1"
PASSWD = "bal8bObG)uvxHbHp"
DB = "BDpython1"
cnx = mysql.connector.connect(user = USER, password = PASSWD, host = SERVER , database = DB )
cursor = cnx.cursor()


sql = "SELECT ruta_archivo FROM Otros_archivos WHERE nombre_archivo = 'Algas.JPG'"
cursor.execute(sql)
results = cursor.fetchall()
for i in results:
            a = f'{i}'.replace("('","")
            Ruta_ima = f'{a}'.replace("',)","")
print(Ruta_ima)