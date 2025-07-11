import mysql.connector
import cv2
from datetime import datetime 
import scipy.io as sio
import numpy as np
import os

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
        
class ArchMAT:
    """Carga y maneja señales desde un archivo .mat"""

    def __init__(self, nombre_archivo, ruta_archivo):
        self.nombre = nombre_archivo
        self.ruta = ruta_archivo
        self.datos_mat = sio.loadmat(ruta_archivo)
        self.senal = self.datos_mat.get('data')  # Asegurarse de tener 'data' como clave

        # En caso de ser 3D, tomar solo la primera época
        if self.senal is not None and self.senal.ndim == 3:
            self.senal = self.senal[:, :, 0]

        self.frecuencia = 100  # Hz (modificable según tu archivo)

    def obtener_llaves(self):
        #---Esto devuelve las claves del archivo .mat---
        return list(self.datos_mat.keys())

    def es_arreglo_valido(self, clave):
        #---Esto para verificar si la clave contiene un arreglo NumPy---
        return isinstance(self.datos_mat.get(clave), np.ndarray)

    def extraer_intervalo(self, clave, canal_ini, canal_fin, tiempo_ini, tiempo_fin):
        arreglo = self.datos_mat.get(clave)
        #--- El arreglo de 3D a 2D---
        if arreglo.ndim == 3:
            arreglo = arreglo[:, :, 0]

        if canal_ini > canal_fin or canal_fin >= arreglo.shape[0]:
            raise ValueError("Rango de canales inválido")

        idx_ini = int(tiempo_ini * self.frecuencia)
        idx_fin = int(tiempo_fin * self.frecuencia)

        if idx_ini >= idx_fin or idx_fin > arreglo.shape[1]:
            raise ValueError("Intervalo de tiempo inválido")

        tiempo = np.arange(idx_ini, idx_fin) / self.frecuencia
        datos = arreglo[canal_ini:canal_fin+1, idx_ini:idx_fin]
        return tiempo, datos

    def calcular_promedio(self, clave):
        arreglo = self.datos_mat.get(clave)
        if arreglo.ndim == 3:
            arreglo = arreglo[:, :, 0]

        if arreglo.ndim != 2:
            raise ValueError("El arreglo debe ser 2D para poder calcular promedio")

        if arreglo.shape[0] <= arreglo.shape[1]:
            promedio = np.mean(arreglo, axis=1)
            indices = np.arange(arreglo.shape[0])
        else:
            promedio = np.mean(arreglo, axis=0)
            indices = np.arange(arreglo.shape[1])

        return indices, promedio