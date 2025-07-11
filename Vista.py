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
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout,
    QSpinBox, QDoubleSpinBox, QMessageBox, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import numpy as np
from Modelo import ArchMAT
import os

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
        # login = self.Campo_User.text()
        # passwd = self.Campo_Passwd.text()
        login = "Jose.R"
        passwd = "loleljuego_01"
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
        self.Button_Cambio_Color.clicked.connect(self.cambio_color)
        self.Button_Ecu_Ima.clicked.connect(self.ecualizacion)
        self.Button_Binarizacion.clicked.connect(self.binarizacion)
        self.Button_Conteo_Celulas.clicked.connect(self.conteo_celulas)

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
        # Eliminar cualquier widget previo en campo_grafico
        for widget in self.campo_grafico.children():
            widget.deleteLater()

        self.img = self.List_imgs.model().data(index, Qt.DisplayRole)
        self.ima = self.__controlador.mostrar_ima(self.img)
        
        if self.ima is not None:
            height, width, channel = self.ima.shape
            bytesPerLine = 3 * width
            q_img = QImage(self.ima.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            
            pixmap = QPixmap.fromImage(q_img)
            pixmap = pixmap.scaled(self.campo_grafico.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            label = QLabel(self.campo_grafico)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setGeometry(self.campo_grafico.rect())
            label.show()
            
            self.Info_ima_Text.setText(f"""- Tamaño, producto de f*col*can: {self.ima.size}
- height: {height}
- width: {width}
- Tipo: {self.ima.dtype}
- Tamaño, D1: {len(self.ima)}
- Tamaño, D2: {len(self.ima[0,:,:])}
- Tamaño, D3: {len(self.ima[0,0,:])}
- F, C, c: {self.ima.shape}
- Media: {self.ima.mean()}
- Desviación Estandar: {self.ima.std()}
- Minimo: {self.ima.min()}
- Maximo: {self.ima.max()}""")
            self.Label_Alert.setText("")
        else:
            self.Info_ima_Text.setText("No se pudo cargar la imagen.")

    def cambio_color(self):
        try:
            for widget in self.campo_grafico.children():
                widget.deleteLater() 
            if self.ima is not None:
                # Convertir la imagen de BGR a RGB
                img_ = cv2.cvtColor(self.ima, cv2.COLOR_BGR2RGB)
                
                # Actualizar self.ima con la imagen convertida
                self.ima = img_
                
                # Actualizar el campo_grafico con la nueva imagen
                height, width, channel = self.ima.shape
                bytesPerLine = 3 * width
                q_img = QImage(self.ima.data, width, height, bytesPerLine, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                pixmap = pixmap.scaled(self.campo_grafico.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # Actualizar el QLabel en campo_grafico
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
                
                # Actualizar la información de la imagen
                self.Info_ima_Text.setText(f"""- Tamaño, producto de 
f*col*can: {self.ima.size}
- height: {height}
- width: {width}
- Tipo: {self.ima.dtype}
- Tamaño, D1: {len(self.ima)}
- Tamaño, D2: {len(self.ima[0,:,:])}
- Tamaño, D3: {len(self.ima[0,0,:])}
- F, C, c: {self.ima.shape}
- Media: {self.ima.mean()}
- Desviación Estandar: {self.ima.std()}
- Minimo: {self.ima.min()}
- Maximo: {self.ima.max()}""")
                self.Label_Alert.setText("")
                
            else:
                self.Info_ima_Text.setText("No hay ninguna imagen cargada.")
        except:
                self.Label_Alert.setText("Asegurese de elegir una imagen.")


    def ecualizacion(self):
        try: 
            for widget in self.campo_grafico.children():
                widget.deleteLater()   
            if self.ima is not None:
                # Convertir la imagen a escala de grises si es a color
                if len(self.ima.shape) == 3:
                    img_gray = cv2.cvtColor(self.ima, cv2.COLOR_BGR2GRAY)
                else:
                    img_gray = self.ima
                
                # Ecualizar la imagen
                img_ecualizada = cv2.equalizeHist(img_gray)
                
                # Crear una figura de matplotlib con dos subfiguras
                fig = Figure(figsize=(10, 5))
                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)
                
                # Mostrar la imagen original y ecualizada
                ax1.imshow(img_gray, cmap='gray')
                ax1.set_title('Original')
                ax1.axis('off')
                
                ax2.imshow(img_ecualizada, cmap='gray')
                ax2.set_title('Ecualizada')
                ax2.axis('off')
                
                # Convertir la figura a un widget de Qt
                canvas = FigureCanvas(fig)
                canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                canvas.updateGeometry()
                
                # Eliminar cualquier widget previo en campo_grafico
                # Primero, eliminamos el layout existente y todos sus widgets
                layout = self.campo_grafico.layout()
                if layout is not None:
                    while layout.count():
                        child = layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    layout.deleteLater()
                
                # Crear un nuevo layout para campo_grafico
                new_layout = QtWidgets.QVBoxLayout(self.campo_grafico)
                new_layout.addWidget(canvas)
                # Actualizar el campo_grafico con el nuevo layout
                self.campo_grafico.setLayout(new_layout)
                self.Label_Alert.setText("")

            else:
                self.Info_ima_Text.setText("No hay ninguna imagen cargada.")
        except:
                self.Label_Alert.setText("Asegurese de elegir una imagen.")
    from matplotlib.figure import Figure

    def binarizacion(self):
        try:
            # Obtener valores del kernel
            row = int(self.Campo_Filas.text())
            col = int(self.Campo_Columnas.text())
            kernel = (row, col)
            
            if self.ima is not None:
                # Eliminar cualquier widget previo en campo_grafico
                for widget in self.campo_grafico.children():
                    widget.deleteLater()

                # Convertir la imagen a escala de grises si es a color
                if len(self.ima.shape) == 3:
                    img_gray = cv2.cvtColor(self.ima, cv2.COLOR_BGR2GRAY)
                else:
                    img_gray = self.ima.copy()  # Asegurarse de no modificar la imagen original
                vmin = np.min(img_gray)
                vmax = np.max(img_gray)
                # Binarización usando Threshold
                _, img_bin = cv2.threshold(img_gray, vmin, vmax, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                imaEro = cv2.erode(img_bin,kernel,iterations = 1)
                imaT = cv2.dilate(imaEro,kernel,iterations = 3)
                # Crear una figura de matplotlib con dos subfiguras
                fig = Figure(figsize=(10, 5))
                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)
                
                # Mostrar la imagen original y binarizada
                ax1.imshow(img_gray, cmap='gray')
                ax1.set_title('Original')
                ax1.axis('off')
                
                ax2.imshow(imaT, cmap='gray')
                ax2.set_title('Binarizada')
                ax2.axis('off')
                
                # Convertir la figura a un widget de Qt
                canvas = FigureCanvas(fig)
                canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                canvas.updateGeometry()
                
                # Eliminar cualquier layout existente y todos sus widgets
                layout = self.campo_grafico.layout()
                if layout is not None:
                    while layout.count():
                        child = layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    layout.deleteLater()
                
                # Crear un nuevo layout para campo_grafico
                new_layout = QtWidgets.QVBoxLayout(self.campo_grafico)
                new_layout.addWidget(canvas)
                
                # Actualizar el campo_grafico con el nuevo layout
                self.campo_grafico.setLayout(new_layout)
                self.Label_Alert.setText("")

            else:
                self.Label_Alert.setText("No hay ninguna imagen cargada.")
        except:
            self.Label_Alert.setText("Asegurese de elegir una imagen.")

    def conteo_celulas(self):
        try:
            if self.ima is not None:
                # Eliminar cualquier widget previo en campo_grafico
                for widget in self.campo_grafico.children():
                    widget.deleteLater()

                # Convertir la imagen a escala de grises si es a color
                if len(self.ima.shape) == 3:
                    img_gray = cv2.cvtColor(self.ima, cv2.COLOR_BGR2GRAY)
                else:
                    img_gray = self.ima.copy()

                # Binarización usando Threshold de Otsu
                _, img_otsu = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Crear kernel para operaciones morfológicas
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (8, 8))

                # Erosión para reducir ruido
                img_erode = cv2.erode(img_otsu, kernel, iterations=1)

                # Dilatación para unir contornos
                img_dilate = cv2.dilate(img_erode, kernel, iterations=1)

                # Conteo de componentes conectados
                num_celulas, mask = cv2.connectedComponents(img_dilate)

                # Crear una figura de matplotlib con dos subfiguras
                fig = Figure(figsize=(10, 5))
                ax1 = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)

                # Mostrar la imagen original y la imagen con máscara
                ax1.imshow(cv2.cvtColor(self.ima, cv2.COLOR_BGR2RGB))
                ax1.set_title('Imagen Original')
                ax1.axis('off')

                ax2.imshow(mask, cmap='inferno')
                ax2.set_title('Máscara de Células')
                ax2.axis('off')

                # Convertir la figura a un widget de Qt
                canvas = FigureCanvas(fig)
                canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                canvas.updateGeometry()

                # Eliminar cualquier layout existente y todos sus widgets
                layout = self.campo_grafico.layout()
                if layout is not None:
                    while layout.count():
                        child = layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    layout.deleteLater()

                # Crear un nuevo layout para campo_grafico
                new_layout = QtWidgets.QVBoxLayout(self.campo_grafico)
                new_layout.addWidget(canvas)

                # Actualizar el campo_grafico con el nuevo layout
                self.campo_grafico.setLayout(new_layout)

                # Actualizar el Label_Alert con el número de células
                self.Label_Alert.setText(f"El número de células en la imagen es de {num_celulas}")
            else:
                self.Label_Alert.setText("No hay ninguna imagen cargada.")
        except Exception as e:
            self.Label_Alert.setText(f"Error: {str(e)}")


class menu_DICOM(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("DICOM_Experto_Imagenes.ui",self) 
        
class menu_Senales(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Menu_Experto-Senales.ui",self) 
        self.setup()

