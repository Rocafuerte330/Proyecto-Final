from PyQt5.QtWidgets import QDialog, QMainWindow, QFileDialog, QListView, QLabel
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Modelo import *
import time
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QImage, QPixmap



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
        self.Button_CargarBD.clicked.connect(self.mostrar_lista)
        self.List_imgs.clicked.connect(self.mostrar_ima)

    def setControlador(self, c):
        self.__controlador = c

    def cargar_Ima(self):
        archivo_cargado, _ = QFileDialog.getOpenFileName(self, "Cargar Imágen","","Imágenes jpg (*.jpg);;Imágenes png (*.png)")
        if archivo_cargado != '':
            print(archivo_cargado)
            #Leemos la imagen con el etodo de opencv
            dataimg =  cv2.imread(archivo_cargado)
            dataimg = cv2.cvtColor(dataimg, cv2.COLOR_BGR2RGB)
            self.__controlador.guardar_Ruta(archivo_cargado)

    def mostrar_lista(self):
        list = self.__controlador.mostrar_lista()
        model = QStringListModel()
        model.setStringList(list)
        self.List_imgs.setModel(model)
        # print(list)

    def mostrar_ima(self, index):
    # Obtener el nombre del elemento seleccionado
        self.img = self.List_imgs.model().data(index, Qt.DisplayRole)
        
        # Obtener la imagen asociada usando el controlador
        self.ima = self.__controlador.mostrar_ima(self.img)
        
        if self.ima is not None:
            # Convertir la imagen de OpenCV a formato compatible con Qt
            height, width, channel = self.ima.shape
            bytesPerLine = 3 * width
            q_img = QImage(self.ima.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            
            # Redimensionar la imagen para que se ajuste al tamaño del campo_grafico
            pixmap = QPixmap.fromImage(q_img)
            pixmap = pixmap.scaled(self.campo_grafico.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Crear un QLabel como hijo del campo_grafico y mostrar la imagen
            label = QLabel(self.campo_grafico)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setGeometry(self.campo_grafico.rect())
            
            # Eliminar cualquier otro QLabel existente en campo_grafico
            for widget in self.campo_grafico.findChildren(QLabel):
                if widget != label:
                    widget.deleteLater()
            
            # Asegurarse de que el QLabel se muestra correctamente
            label.show()
        else:
            print("No se pudo cargar la imagen.")
        
        

class menu_DICOM(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("DICOM_Experto_Imagenes.ui",self) 
        
class menu_Senales(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Menu_Experto-Senales.ui",self) 
        self.setup()

