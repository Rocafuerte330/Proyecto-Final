from PyQt5.QtWidgets import QDialog, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Modelo import *
import time
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class VentanaLogin(QDialog):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Login.ui", self)
        self.__controlador = None
        self.setup()
    
    def setup(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
# Si probamos veremos que la ventana se cerrará, algo que no queremos para el ejemplo, por lo que será mejor sobre-escribir los
# métodos accept y reject que por defecto cierran la ventana
    def accept(self):
        login = self.Campo_User.text()
        passwd = self.Campo_Passwd.text()
        # login = "Jose.R"
        # passwd = "loleljuego_01"
# Pasamos la información al controlaror
        resultado = self.__controlador.validarUsuario(login,passwd)
# Imprimimos el resultado de la operación
        if resultado == "Experto en Imágenes":
            self.buttonBox.accepted.connect(self.abrir_menu_imagenes)
        elif resultado == "Experto en Señales":
            self.buttonBox.accepted.connect(self.abrir_menu_senales)
        else:
            self.label.setText("Usuario no encontrado\nIntente nuevamente")
            
    def reject(self):
        self.Campo_User.setText("")
        self.Campo_Passwd.setText("")

# Sobre escribir este método nos implica también reescribir el método closeEvent()

    def closeEvent(self, event):
        print("Cerrando ventana")
        self.close()

#programamos un método para que pueda recibirlo
    def setControlador(self, c):
        self.__controlador = c

    def abrir_menu_imagenes(self):
        menuImagenes = menu_Imagenes(self)
        menuImagenes.setControlador(self.__controlador)  # Configurar el controlador
        self.hide()
        menuImagenes.show()
    
    def abrir_menu_senales(self):
        menuSeñales = menu_Senales(self)
        self.hide()
        menuSeñales.show()
    
class menu_Imagenes(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Menu_Experto_Imagenes.ui",self)
        self.__controlador = None  # Inicializa el atributo __controlador
        self.setup()

    def setup(self):
        self.Button_JPG_PNG.clicked.connect(self.abrir_menu_JPG_PNG)
        self.Button_DICOM.clicked.connect(self.abrir_menu_DICOM)

    def abrir_menu_JPG_PNG(self):
        menuJPG_PNG = menu_JPG_PNG(self)
        menuJPG_PNG.setControlador(self.__controlador)  # Configurar el controlador
        self.hide()
        menuJPG_PNG.show()
    

    def abrir_menu_DICOM(self):
        menuDICOM = menu_DICOM(self)
        self.hide()
        menuDICOM.show()

    def setControlador(self, c):
        self.__controlador = c

class menu_JPG_PNG(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("JPG_PNG_Experto_Imagenes.ui",self) 
        self.__controlador = None  # Inicializa el atributo __controlador
        self.setup()

    def setup(self):
        self.Button_Cargar_Ima.clicked.connect(self.cargar_Ima)

    def setControlador(self, c):
        self.__controlador = c

    def cargar_Ima(self):
        archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Cargar Imágen","","Imágenes jpg (*.jpg);;Imágenes png (*.png)")
        if archivo_cargado != '':
            print(archivo_cargado)
            #Leemos la imagen con el etodo de opencv
            dataimg =  cv2.imread(archivo_cargado)
            dataimg = cv2.cvtColor(dataimg, cv2.COLOR_BGR2RGB)

class menu_DICOM(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("DICOM_Experto_Imagenes.ui",self) 
        
class menu_Senales(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Menu_Experto-Senales.ui",self) 
        self.setup()

