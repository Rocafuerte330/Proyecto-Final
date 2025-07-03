from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Modelo import *
import time


class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Login.ui", self)
        self.setup()
    
    def setup(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
# Si probamos veremos que la ventana se cerrará, algo que no queremos para el ejemplo, por lo que será mejor sobre-escribir los
# métodos accept y reject que por defecto cierran la ventana
    def accept(self):
        login = self.Campo_User.text()
        passwd = self.Campo_Passwd.text()
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

class menu_Senales(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("Menu_Experto-Senales.ui",self) 