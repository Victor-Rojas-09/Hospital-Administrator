"""
Punto de entrada principal (__main__) de la aplicación.
"""
import sys
from PyQt6.QtWidgets import QApplication

from controller.hospital_controller import HospitalController
from GUI.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    hospital_controller = HospitalController()

    ventana_principal = MainWindow(controller=hospital_controller)

    ventana_principal.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()