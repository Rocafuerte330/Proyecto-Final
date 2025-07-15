import mysql.connector
import cv2
from datetime import datetime 
from scipy.io import loadmat
import scipy.io as sio
import numpy as np
import pandas as pd
import os

SERVER = "localhost"
USER = "BDpython1"
PASSWD = "bal8bObG)uvxHbHp"
DB = "BDpython1"
cnx = mysql.connector.connect(user = USER, password = PASSWD, host = SERVER , database = DB )
cursor = cnx.cursor()


class BaseDatos(object):
    def __init__(self, nombre="", ruta=""):
        self.login = ""
        self.passwd = ""
        self.nombre = nombre
        self.ruta = ruta
        self.datos   = None
        self.dataframe = None
        self.frecuencia = 100
        self.senal = None

    def cargar_mat(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)
        self.datos = loadmat(ruta)
        self.frecuencia = self.datos.get('fs', 100)

    def cargar_csv(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)
        self.dataframe = pd.read_csv(ruta)
        

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
        sql = "SELECT nombre_archivo FROM Otros_archivos WHERE tipo_archivo IN (%s, %s, %s)"
        cursor.execute(sql, ("jpg", "png", None))
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

    def obtener_llaves(self):
        return [k for k in self.datos.keys() if not k.startswith("__")]

    def es_arreglo_valido(self, clave):
        try:
            self.senal = self.datos[clave]
            if isinstance(self.senal, np.ndarray):
                if self.senal.ndim == 3:
                    self.senal = self.senal[:, :, 0]
                elif self.senal.ndim > 3:
                    return False
                return self.senal.ndim == 2 and np.issubdtype(self.senal.dtype, np.number)
            return False
        except:
            return False

    def extraer_intervalo(self, clave, canal_ini, canal_fin, tiempo_ini, tiempo_fin):
        self.senal = self.datos[clave]
        if self.senal.ndim == 3:
            self.senal = self.senal[:, :, 0]
        if self.senal.ndim != 2:
            raise ValueError("El arreglo debe ser bidimensional")
        if canal_ini < 0 or canal_fin >= self.senal.shape[0] or canal_ini > canal_fin:
            raise ValueError("Rango de canales inválido")
        idx_ini = int(tiempo_ini * self.frecuencia)
        idx_fin = int(tiempo_fin * self.frecuencia)
        if idx_ini < 0 or idx_fin > self.senal.shape[1] or idx_ini >= idx_fin:
            raise ValueError("Intervalo de tiempo inválido")
        datos = self.senal[canal_ini:canal_fin + 1, idx_ini:idx_fin]
        tiempo = np.arange(idx_ini, idx_fin) / self.frecuencia
        return tiempo, datos

    def calcular_promedio(self, clave):
        arreglo = self.datos[clave]
        print(f"Depuración - Clave: {clave}, Tipo: {type(arreglo)}, Shape: {getattr(arreglo, 'shape', 'No shape')}")

        if arreglo.ndim == 3:
            arreglo = arreglo[:, :, 0]
        elif arreglo.ndim > 3:
            raise ValueError("Arreglo con más de 3 dimensiones no soportado")
        if arreglo.ndim != 2:
            raise ValueError("La clave seleccionada no es un arreglo bidimensional válido")
        if arreglo.size == 0:
            raise ValueError("El arreglo está vacío")
        if not np.issubdtype(arreglo.dtype, np.number):
            raise ValueError("El arreglo contiene datos no numéricos")

        arreglo = np.nan_to_num(arreglo, nan=0.0, posinf=0.0, neginf=0.0)
        try:
            promedio = np.mean(arreglo, axis=1)
            if len(promedio) == 0:
                raise ValueError("El promedio calculado está vacío")
            indices = np.arange(len(promedio))
            return indices, promedio
        except Exception as e:
            raise ValueError(f"Error en cálculo de promedio: {str(e)}")


    def obtener_columnas(self):
        return self.dataframe.columns.tolist()

    def obtener_valores(self, columna_x, columna_y):
        if columna_x not in self.dataframe.columns or columna_y not in self.dataframe.columns:
            raise ValueError("Columna no encontrada")
        return self.dataframe[columna_x].values, self.dataframe[columna_y].values

    def calcular_promedios(self):
        return self.dataframe.mean(numeric_only=True)

    def calcular_estadisticas(self, columna):
        if columna not in self.dataframe.columns:
            raise ValueError("Columna no encontrada")
        datos = self.dataframe[columna]
        return {
            'media': datos.mean(),
            'mediana': datos.median(),
            'desviacion': datos.std(),
            'minimo': datos.min(),
            'maximo': datos.max()
        }

    def obtener_datos_tabla(self):
        return self.dataframe.values.tolist(), self.dataframe.columns.tolist()
    

    def guardar_DICOM(self, Ruta):
        listR = Ruta.split("/")
        a = len(listR)
        nombre_carpeta = listR[a-1]
        sql_insert = f"""INSERT  INTO  DICOM_NIFTI (Nombre_Carpeta, Ruta_Dicom)
                                    VALUES (%s, %s)"""
        cursor.execute(sql_insert,(nombre_carpeta, Ruta ))
        cnx.commit()
    
    def mostrar_lista_dicom(self):
        list = []
        sql = "SELECT Nombre_Carpeta FROM DICOM_NIFTI"
        cursor.execute(sql)
        results = cursor.fetchall()
        for i in results:
            a = f'{i}'.replace("('","")
            b = f'{a}'.replace("',)","")
            list.append(b)
        return list
    
    def obtener_ruta_dicom(self, nombre_carpeta):
        sql = "SELECT Ruta_Dicom FROM DICOM_NIFTI WHERE Nombre_Carpeta = %s"
        cursor.execute(sql, (nombre_carpeta,))
        result = cursor.fetchone()
        return result[0] if result else None