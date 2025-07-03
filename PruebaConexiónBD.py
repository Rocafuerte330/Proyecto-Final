#Conexion a base de datos
import mysql.connector

SERVER = "localhost"
USER = "BDpython1"
PASSWD = "bal8bObG)uvxHbHp"
DB = "BDpython1"
cnx = mysql.connector.connect(user = USER, password = PASSWD, host = SERVER , database = DB )
cursor = cnx.cursor()


# sql = "SELECT * FROM Usuarios"
# cursor.execute(sql)
# results = cursor.fetchall()
# print(results)

login = "Jose.R"
passwd = "loleljuego_01"

sql = "SELECT nombre_usuario FROM Usuarios"
cursor.execute(sql)
results = cursor.fetchall()
for i in results:
    a = f'{i}'.replace("('","")
    b = f'{a}'.replace("',)","")
    if b == login:
        c = True
        break
    else:
        c = False

sql = "SELECT contrasena FROM Usuarios"
cursor.execute(sql)
results = cursor.fetchall()
for i in results:
    a = f'{i}'.replace("('","")
    b = f'{a}'.replace("',)","")
    if b == passwd:
        d = True
        break
    else:
        d = False

sql = f"SELECT tipo_usuario FROM Usuarios WHERE nombre_usuario = '{login}' AND contrasena = '{passwd}'"
cursor.execute(sql)
results = cursor.fetchall()
a = f'{results}'.replace("[('","")
b = f'{a}'.replace("',)]","")
print(b)

