# Acá se haría el enlace y se inicia el programa
from Modelo import *
from Vista import *
import sys
from PyQt5.QtWidgets import QApplication

class Coordinador():
    # El coordinador debe tenet acceso a obejetos de ambas clases (Modelo y vista)
    def __init__(self, vista, modelo):
        self.__vista = vista
        self.__modelo = modelo
# El controlador debe tener un método para recibir la información de la vista.
# El controlador simplemente debe enviar esta info al modelo y esperar que este le responda
    def validarUsuario(self, login, passwd):
        # asignando valores al modelo
        self.__modelo.setLogin(login)
        self.__modelo.setPasswd(passwd)
        return self.__modelo.ValidarUsuario(login, passwd)

def main():
    app = QApplication(sys.argv)
    vista = VentanaLogin()
    modelo = BaseDatos()
    coordinador = Coordinador(vista, modelo)
#En el método main le asignamos este controlador a la ventana
    vista.setControlador(coordinador)
    
    vista.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()