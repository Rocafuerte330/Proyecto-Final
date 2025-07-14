from PyQt5.QtWidgets import QDialog, QMainWindow, QFileDialog, QListView, QLabel, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Modelo import *
import time
import cv2
from PyQt5.QtGui import QIcon
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
from Modelo import BaseDatos
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
        login = self.Campo_User.text()
        passwd = self.Campo_Passwd.text()
        resultado = self.__controlador.validarUsuario(login, passwd)

        if resultado == "Experto en Imágenes":
            self.abrir_menu_imagenes()          # ← directo
        elif resultado == "Experto en Señales":
            self.abrir_menu_senales()           # ← directo
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
        menuSenales = menu_Senales(self)
        menuSenales.setControlador(self.__controlador)  # ← NUNCA olvides esta línea
        self.hide()
        menuSenales.show()
    
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
            self.Label_Alert.setText("Asegurese de elegir una imagen y que el kernel sean numeros enteros.")

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

                vmin = np.min(img_gray)
                vmax = np.max(img_gray)
                # Binarización usando Threshold de Otsu
                _, img_otsu = cv2.threshold(img_gray, vmin, vmax, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                # Crear kernel para operaciones morfológicas
                row = int(self.Campo_Filas.text())
                col = int(self.Campo_Columnas.text())
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (row, col))

                iter = int(self.Campo_iter.text())
                # Erosión para reducir ruido
                img_erode = cv2.erode(img_otsu, kernel, iterations=iter)

                # Dilatación para unir contornos
                img_dilate = cv2.dilate(img_erode, kernel, iterations=iter)

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
                self.Label_Alert.setText(f"El número de células en la imagen es de {num_celulas-1}")
            else:
                self.Label_Alert.setText("No hay ninguna imagen cargada.")
        except Exception as e:
            self.Label_Alert.setText(f"Asegurese de elegir una imagen y que el kernel sean numeros enteros")


class menu_DICOM(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("DICOM_Experto_Imagenes.ui",self) 
        
class menu_Senales(QMainWindow):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("Menu_Experto-Senales.ui", self)
        self.__controlador = None
        self.archivo_mat = None
        self.archivo_csv = None
        self.canvas_mat = None  # Nueva referencia fuerte
        self.canvas_csv = None  # Nueva referencia fuerte
        self.setup()

    def setup(self):
        self.btnCargarMat.clicked.connect(self.cargar_mat)
        self.btnGraficarMat.clicked.connect(self.graficar_mat)
        self.btnPromedioMat.clicked.connect(self.promedio_mat)
        self.btnCargarCSV.clicked.connect(self.cargar_csv)
        self.btnGraficarScatter.clicked.connect(self.graficar_scatter_csv)
        self.btnPromedioCSV.clicked.connect(self.promedio_csv)
        self.btnSalir.clicked.connect(self.close)

        self.figure_mat = Figure()
        self.canvas_mat = FigureCanvas(self.figure_mat)  # Asignar a la referencia fuerte
        layout_mat = QVBoxLayout(self.widget_2)
        layout_mat.addWidget(self.canvas_mat)
        self.widget_2.setLayout(layout_mat)

        self.figure_csv = Figure()
        self.canvas_csv = FigureCanvas(self.figure_csv)  # Asignar a la referencia fuerte
        layout_csv = QVBoxLayout(self.widget_4)
        layout_csv.addWidget(self.canvas_csv)
        self.widget_4.setLayout(layout_csv)

        self.setStyleSheet("""
            QMainWindow { background-color: rgb(239, 239, 239); }
            QPushButton { background-color: rgb(167, 188, 217); color: white; border-radius: 5px; padding: 8px; font-family: Times New Roman; font-size: 12pt; }
            QPushButton#btnCargarMat, QPushButton#btnCargarCSV { background-color: rgb(177, 200, 230); }
            QPushButton#btnSalir { background-color: rgb(211, 211, 211); }
            QComboBox, QLineEdit { background-color: rgb(255, 255, 255); border: 1px solid rgb(223, 223, 223); padding: 5px; font-family: Times New Roman; font-size: 12pt; }
            QTableWidget { background-color: rgb(255, 255, 255); border: 1px solid rgb(223, 223, 223); }
        """)

        self.btnCargarMat.setIcon(QIcon("Escudo-UdeA.svg"))
        self.btnCargarCSV.setIcon(QIcon("Escudo-UdeA.svg"))
        self.btnSalir.setIcon(QIcon("icono de usuario.webp"))

    def setControlador(self, c):
        self.__controlador = c

    def cargar_mat(self):
        if self.__controlador is None:
            QMessageBox.critical(self, "Error", "Controlador no asignado.")
            return
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar archivo .mat", "", "Archivos MAT (*.mat)")
        if ruta:
            try:
                self.__controlador.cargar_mat(ruta)
                self.archivo_mat = self.__controlador.archivo_mat
                llaves = self.archivo_mat.obtener_llaves()
                validas = [k for k in llaves if self.archivo_mat.es_arreglo_valido(k)]
                if validas:
                    self.comboLlaves.clear()
                    self.comboLlaves.addItems(validas)
                else:
                    QMessageBox.critical(self, "Error", "No se encontraron claves válidas.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo .mat: {str(e)}")

    def graficar_mat(self):
        if not self.archivo_mat:
            QMessageBox.warning(self, "Error", "Primero cargue un archivo .mat.")
            return
        try:
            clave = self.comboLlaves.currentText()
            c_ini = int(self.inputCanalIni.text())
            c_fin = int(self.inputCanalFin.text())
            t_ini = float(self.inputTiempoIni.text())
            t_fin = float(self.inputTiempoFin.text())
            tiempo, datos = self.__controlador.extraer_intervalo(clave, c_ini, c_fin, t_ini, t_fin)

            self.figure_mat.clear()
            ax = self.figure_mat.add_subplot(111)
            for i, canal in enumerate(datos):
                ax.plot(tiempo, canal, label=f"Canal {c_ini + i + 1}")
            ax.set_title("Señales Biomédicas", fontfamily="Times New Roman", fontsize=14)
            ax.set_xlabel("Tiempo (s)", fontfamily="Times New Roman")
            ax.set_ylabel("Amplitud", fontfamily="Times New Roman")
            ax.legend()
            ax.grid(True)
            self.canvas_mat.draw()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

    def promedio_mat(self):
        if not self.archivo_mat:
            QMessageBox.warning(self, "Error", "Primero cargue un archivo .mat.")
            return
        try:
            clave = self.comboLlaves.currentText()
            indices, promedio = self.__controlador.calcular_promedio(clave)

            self.figure_mat.clear()
            ax = self.figure_mat.add_subplot(111)
            ax.stem(indices, promedio)
            ax.set_title("Promedio por Canal", fontfamily="Times New Roman", fontsize=14)
            ax.set_xlabel("Canal", fontfamily="Times New Roman")
            ax.set_ylabel("Amplitud Promedio", fontfamily="Times New Roman")
            ax.grid(True)
            self.canvas_mat.draw()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular promedio: {str(e)}")

    def cargar_csv(self):
        if self.__controlador is None:
            QMessageBox.critical(self, "Error", "Controlador no asignado.")
            return
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar archivo CSV", "", "Archivos CSV (*.csv)")
        if ruta:
            try:
                self.__controlador.cargar_csv(ruta)
                self.archivo_csv = self.__controlador.archivo_csv
                datos, columnas = self.archivo_csv.obtener_datos_tabla()
                self.tablaCSV.setRowCount(len(datos))
                self.tablaCSV.setColumnCount(len(columnas))
                self.tablaCSV.setHorizontalHeaderLabels(columnas)
                for i, row in enumerate(datos):
                    for j, val in enumerate(row):
                        self.tablaCSV.setItem(i, j, QTableWidgetItem(str(val)))
                columnas = self.archivo_csv.obtener_columnas()
                self.comboColumnaX.clear()
                self.comboColumnaY.clear()
                self.comboColumnaX.addItems(columnas)
                self.comboColumnaY.addItems(columnas)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo CSV: {str(e)}")

    def graficar_scatter_csv(self):
        if not self.archivo_csv:
            QMessageBox.warning(self, "Error", "Primero cargue un archivo CSV.")
            return
        try:
            col_x = self.comboColumnaX.currentText()
            col_y = self.comboColumnaY.currentText()
            x, y = self.__controlador.obtener_valores_csv(col_x, col_y)

            self.figure_csv.clear()
            ax = self.figure_csv.add_subplot(111)
            ax.scatter(x, y, color='blue', alpha=0.5)
            ax.set_title(f"Dispersión: {col_x} vs {col_y}", fontfamily="Times New Roman", fontsize=14)
            ax.set_xlabel(col_x, fontfamily="Times New Roman")
            ax.set_ylabel(col_y, fontfamily="Times New Roman")
            ax.grid(True)
            self.canvas_csv.draw()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

    def promedio_csv(self):
        if not self.archivo_csv:
            QMessageBox.warning(self, "Error", "Primero cargue un archivo CSV.")
            return
        try:
            promedios = self.__controlador.calcular_promedios_csv()
            columnas = promedios.index
            valores = promedios.values

            self.figure_csv.clear()
            ax = self.figure_csv.add_subplot(111)
            ax.bar(columnas, valores, color='purple')
            ax.set_title("Promedio de Columnas", fontfamily="Times New Roman", fontsize=14)
            ax.set_ylabel("Valor Promedio", fontfamily="Times New Roman")
            ax.grid(True)
            self.canvas_csv.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular promedios: {str(e)}")

    def closeEvent(self, event):
        self.canvas_mat = None  # Limpiar referencias
        self.canvas_csv = None
        self.close()

