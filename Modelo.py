import mysql.connector
import cv2
from datetime import datetime 

SERVER = "localhost"
USER = "BDpython1"
PASSWD = "bal8bObG)uvxHbHp"
DB = "BDpython1"
cnx = mysql.connector.connect(user = USER, password = PASSWD, host = SERVER , database = DB )
cursor = cnx.cursor()


class BaseDatos(object):
    def __init__(self):
        self.login = ""
        self.passwd = ""

    def setLogin(self, login):
        self.login = login

    def setPasswd(self, passwd):
        self.passwd = passwd

    def ValidarUsuario(self, login, passwd):
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

        if (c and d) == True:
            sql = f"SELECT tipo_usuario FROM Usuarios WHERE nombre_usuario = '{login}' AND contrasena = '{passwd}'"
            cursor.execute(sql)
            results = cursor.fetchall()
            a = f'{results}'.replace("[('","")
            b = f'{a}'.replace("',)]","")
            return b
        else:
            print("Usuario no encontrado.")
    
    def guardar_Ruta(self, Ruta):
        listR = Ruta.split("/")
        a = len(listR)
        nombre_archivo = listR[a-1]
        if (Ruta.endswith(".jpg") or Ruta.endswith(".JPG"))== True:
            sql_insert = f"""INSERT  INTO  otros_archivos (id_archivo, tipo_archivo, nombre_archivo, fecha_trabajo, ruta_archivo)
                                    VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(sql_insert,(None, "jpg", nombre_archivo, datetime.now(), Ruta ))
            cnx.commit()
        elif (Ruta.endswith(".png") or Ruta.endswith(".JPG")) == True:
            sql_insert = f"""INSERT  INTO  otros_archivos (id_archivo, tipo_archivo, nombre_archivo, fecha_trabajo, ruta_archivo)
                                    VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(sql_insert,(None, "png", nombre_archivo, datetime.now(), Ruta ))
            cnx.commit()
        else: 
            sql_insert = f"""INSERT  INTO  otros_archivos (id_archivo, tipo_archivo, nombre_archivo, fecha_trabajo, ruta_archivo)
                                    VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(sql_insert,(None, None, nombre_archivo, datetime.now(), Ruta ))
            cnx.commit()
    
    def mostrar_lista(self):
        list = []
        sql = "SELECT nombre_archivo FROM Otros_archivos"
        #  WHERE tipo_archivo IN (%s, %s, %s)
        cursor.execute(sql)
        # , ("jpg", "png", None)
        results = cursor.fetchall()
        for i in results:
            a = f'{i}'.replace("('","")
            b = f'{a}'.replace("',)","")
            list.append(b)
        return list
    
    def mostrar_ima(self, nombre_ima):
        sql = f"SELECT ruta_archivo FROM Otros_archivos WHERE nombre_archivo = '{nombre_ima}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        for i in results:
                    a = f'{i}'.replace("('","")
                    Ruta_ima = f'{a}'.replace("',)","")
        print(Ruta_ima)
        return Ruta_ima
        
