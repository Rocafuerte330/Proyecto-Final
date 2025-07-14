# Acá se haría el enlace y se inicia el programa
from Modelo import *
from Vista import *
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
import matplotlib.pyplot as plt

class Coordinador():
    # El coordinador debe tenet acceso a obejetos de ambas clases (Modelo y vista)
    def __init__(self, vista, modelo):
        self.__vista = vista
        self.__modelo = modelo
        self.vista_mat = None
        self.archivo_mat = None
        self.archivo_csv = None
        # Configuración de la base de datos
        self.__db_config = {
            'host': '127.0.0.1',
            'user': 'root',  # Reemplaza con tu usuario de MySQL
            'password': '',  # Reemplaza con tu contraseña
            'database': 'BDpython1'
        }
        self.__conn = None
        self.__cursor = None
        try:
            self.__conn = mysql.connector.connect(**self.__db_config)
            self.__cursor = self.__conn.cursor()
            print(f"Conexión a MySQL establecida a las {datetime.now()}")
        except mysql.connector.Error as err:
            print(f"Error de conexión a las {datetime.now()}: {err}")
            QMessageBox.critical(None, "Error", f"No se pudo conectar a la base de datos: {err}")
            sys.exit(1)

    def cleanup(self):
        if self.__cursor:
            self.__cursor.close()
            print(f"Cursor cerrado a las {datetime.now()}")
        if self.__conn:
            self.__conn.close()
            print(f"Conexión a MySQL cerrada a las {datetime.now()}")
    
    def mostrar_vista_senales(self):
        self.vista_mat = menu_Senales()
        self.vista_mat.setControlador(self)
        self.__vista.hide()
        self.vista_mat.show()

    def cargar_mat(self, ruta):
        try:
            self.archivo_mat = BaseDatos()
            self.archivo_mat.cargar_mat(ruta)
            self.guardar_ruta(ruta, 'mat')
            return True
        except Exception as e:
            raise Exception(f"No se pudo cargar el archivo .mat: {str(e)}")
        
    def extraer_intervalo(self, clave, canal_ini, canal_fin, tiempo_ini, tiempo_fin):
        if not self.archivo_mat:
            raise Exception("No hay un archivo .mat cargado")
        if not self.archivo_mat.es_arreglo_valido(clave):
            raise ValueError("La clave seleccionada no es un arreglo válido")
        return self.archivo_mat.extraer_intervalo(clave, canal_ini, canal_fin, tiempo_ini, tiempo_fin)

    def calcular_promedio(self, clave):
        if not self.archivo_mat:
            raise Exception("No hay un archivo .mat cargado")
        if not self.archivo_mat.es_arreglo_valido(clave):
            raise ValueError("La clave seleccionada no es un arreglo válido")
        return self.archivo_mat.calcular_promedio(clave)

    def cargar_csv(self, ruta):
        try:
            self.archivo_csv = BaseDatos()
            self.archivo_csv.cargar_csv(ruta)
            self.guardar_ruta(ruta, 'csv')
            return True
        except Exception as e:
            raise Exception(f"No se pudo cargar el archivo CSV: {str(e)}")

    def obtener_valores_csv(self, columna_x, columna_y):
        if not self.archivo_csv:
            raise Exception("No hay un archivo CSV cargado")
        return self.archivo_csv.obtener_valores(columna_x, columna_y)

    def calcular_promedios_csv(self):
        if not self.archivo_csv:
            raise Exception("No hay un archivo CSV cargado")
        return self.archivo_csv.calcular_promedios()

    def guardar_ruta(self, ruta, tipo):
        if not self.__cursor:
            raise Exception("No hay conexión a la base de datos")
        nombre = os.path.basename(ruta)
        try:
            self.__cursor.execute(
                "INSERT INTO Otros_archivos (tipo_archivo, nombre_archivo, fecha_trabajo, ruta_archivo) VALUES (%s, %s, CURDATE(), %s)",
                (tipo, nombre, ruta)
            )
            self.__conn.commit()
            print(f"Ruta guardada correctamente: {ruta} a las {datetime.now()}")
        except mysql.connector.Error as err:
            self.__conn.rollback()
            print(f"Error al guardar ruta a las {datetime.now()}: {err}")
            raise Exception(f"Error al guardar ruta: {err}")
# El controlador debe tener un método para recibir la información de la vista.
# El controlador simplemente debe enviar esta info al modelo y esperar que este le responda
    def validarUsuario(self, login, passwd):
        # asignando valores al modelo
        self.__modelo.setLogin(login)
        self.__modelo.setPasswd(passwd)
        return self.__modelo.ValidarUsuario(login, passwd)
        
    def guardar_Ruta(self, Ruta):
        self.__modelo.guardar_Ruta(Ruta)
    
    def mostrar_lista(self):
        return self.__modelo.mostrar_lista()
    
    def mostrar_ima(self, nombre_ima):
        Ruta_ima = self.__modelo.mostrar_ima(nombre_ima)
        ima = cv2.imread(Ruta_ima)
        return ima

def main():
    app = QApplication(sys.argv)

    modelo = BaseDatos()          # 1. Crear el modelo
    vista = VentanaLogin()     # 2. Crear la vista
    coordinador = Coordinador(vista, modelo)  # 3. Pasar ambos al coordinador

    vista.setControlador(coordinador)
    vista.show()

    try:
        sys.exit(app.exec_())
    finally:
        coordinador.cleanup()

if __name__ == "__main__":
    main()