#Conexion a base de datos
import mysql.connector

SERVER = "localhost"
USER = "BDpython1"
PASSWD = "bal8bObG)uvxHbHp"
DB = "BDpython1"
cnx = mysql.connector.connect(user = USER, password = PASSWD, host = SERVER , database = DB )
cursor = cnx.cursor()


sql = "SELECT * FROM Usuarios"
cursor.execute(sql)
results = cursor.fetchall()
print(results)

