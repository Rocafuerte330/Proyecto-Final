from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import cv2
import sys
import matplotlib.pyplot as plt

import os
#Seleccionar un archivo desde navegador de archivos
def seleccionar_archivo():
    app = QApplication([])
    archivo, _ = QFileDialog.getOpenFileName(
        None,
        "Selecciona un archivo",
        "",
        "Todos los archivos (*);;Archivos de texto (*.txt)"
    )
    print("Archivo seleccionado:", archivo)
    return archivo

#Seleccionar una carpeta desde navegador de archivos
def seleccionar_carpeta():
    app = QApplication([])

    # Abre el diálogo para seleccionar una carpeta
    carpeta = QFileDialog.getExistingDirectory(
        None,
        "Selecciona una carpeta",
        "/ruta/directorio/inicial",  # Directorio inicial (opcional)
        QFileDialog.ShowDirsOnly  # Muestra solo directorios
    )

    # Imprime la ruta de la carpeta seleccionada
    print("Carpeta seleccionada:", carpeta)
    return carpeta

o = os.listdir(seleccionar_carpeta())
for i in o:
    print("- ", i)

a = seleccionar_archivo()
ima=cv2.imread(a) #Se lee la imagen con OpenCv y se muetsra con matplotlib
imap = cv2.cvtColor(ima, cv2.COLOR_BGR2RGB)
plt.imshow(imap)
plt.show()

def mostrar_mensaje():
    app = QApplication([])

    # Crear una instancia de QMessageBox
    mensaje = QMessageBox()

    # Configurar el mensaje
    mensaje.setWindowTitle("Confirmación")
    mensaje.setText("¿Estás seguro de que quieres continuar?")
    mensaje.setIcon(QMessageBox.Question)
    mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    mensaje.setDefaultButton(QMessageBox.No)  # Establece el botón predeterminado

    # Mostrar el mensaje y obtener la respuesta
    respuesta = mensaje.exec_()

    # Actuar según la respuesta
    if respuesta == QMessageBox.Yes:
        print("El usuario hizo clic en Sí.")
    else:
        print("El usuario hizo clic en No.")

mostrar_mensaje()
