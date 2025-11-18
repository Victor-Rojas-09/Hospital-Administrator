import sys
from PyQt6.QtWidgets import (
    QWidget, QTableWidgetItem, QHeaderView, QApplication,
    QDialog, QLabel, QDialogButtonBox, QStyle
)
from PyQt6.QtGui import QPixmap  # Para manejar los iconos
from PyQt6.uic import loadUi  # La función clave para cargar .ui
from PyQt6.QtCore import Qt

# Importamos el controlador desde su módulo
from controller.hospital_controller import HospitalController


# Output_Window.ui
class OutputWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        try:
            # Carga el diseño desde la carpeta ui_form_QT
            loadUi("ui_form_QT/Output_Window.ui", self)
        except FileNotFoundError:
            # Error fatal si no encontramos el .ui
            print("Error fatal: No se encontró 'Output_Window.ui'.")
            print("Asegúrate de que esté en la carpeta 'ui_form_QT'.")
            sys.exit(1)

        # Conectar el botón OK (aceptar) para cerrar la ventana
        self.button_box.accepted.connect(self.accept)

    def set_message(self, titulo: str, mensaje: str, tipo: str = "info"):
        """
        Configura el diálogo con el mensaje y el icono correctos.
        Usa QStyle para obtener los iconos estándar del sistema.
        """
        self.setWindowTitle(titulo)
        self.message_label.setText(mensaje)

        # Seleccionar icono estándar del sistema (como en tus ejemplos)
        if tipo == "exito":
            pixmap = self.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxInformation)
        elif tipo == "error":
            pixmap = self.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxCritical)
        else:  # "info"
            pixmap = self.style().standardPixmap(QStyle.StandardPixmap.SP_MessageBoxInformation)

        # Asignar el icono al label y escalarlo
        self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))


# MainWindow.ui
class MainWindow(QWidget):

    def __init__(self, controller: HospitalController):
        super().__init__()

        # Dependencias (SOLID)
        self._controller = controller

        # Carga del archivo .ui
        try:
            # Carga el diseño de la ventana principal
            loadUi("ui_form_QT/MainWindow.ui", self)
        except FileNotFoundError:
            print("Error fatal: No se encontró 'MainWindow.ui'.")
            print("Asegúrate de que esté en la carpeta 'ui_form_QT'.")
            sys.exit(1)

        self.setWindowTitle("Sistema de Información Hospitalaria")

        # Conectar señales (clicks) a slots (métodos)
        self.conectar_eventos()

        # Configurar la tabla de resultados
        self.configurar_tabla()

    def configurar_tabla(self):
        """
        Configuraciones iniciales de la tabla de resultados.
        """
        # Asumiendo que el QTableWidget en tu .ui se llama 'tabla_resultados'
        self.tabla_resultados.setColumnCount(4)
        self.tabla_resultados.setHorizontalHeaderLabels(
            ["DNI", "Nombre", "Especialidad", "Hospital"]
        )
        # Evitar que el usuario edite la tabla
        self.tabla_resultados.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        # Ajustar columnas al ancho de la ventana
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def conectar_eventos(self):
        """
        Conecta los botones (señales) a sus funciones (slots).
        """
        self.hospital_create_button.clicked.connect(self.crear_hospital)
        self.add_doctor_button.clicked.connect(self.agregar_doctor)
        self.search_button.clicked.connect(self.buscar_doctor)

    # --- SLOTS ---

    def crear_hospital(self):
        """
        Toma los datos de la UI y los pasa al controlador.
        """
        # 1. Lee los datos de la UI
        nombre = self.hospital_name_input.text()

        # 2. Le pasa los datos al CONTROLADOR
        exito, mensaje = self._controller.crear_hospital(nombre)

        # 3. muestra el resultado
        self.mostrar_dialogo("Crear Hospital", mensaje, "exito" if exito else "error")

    def agregar_doctor(self):
        """
        Toma los datos del doctor y los pasa al controlador.
        """
        # 1. La VISTA lee los datos
        dni = self.doc_dni_input.text()
        nombre = self.doc_name_input.text()
        especialidad = self.doc_spec_input.text()

        # 2. La VISTA le pasa los datos al CONTROLADOR
        exito, mensaje = self._controller.agregar_doctor(dni, nombre, especialidad)

        # 3. La VISTA muestra el resultado
        self.mostrar_dialogo("Agregar Doctor", mensaje, "exito" if exito else "error")

        if exito:
            # Limpiar campos tras éxito (buena práctica de UX)
            self.doc_dni_input.clear()
            self.doc_name_input.clear()
            self.doc_spec_input.clear()

    def buscar_doctor(self):
        """
        Toma el DNI y pide al controlador que busque.
        """
        dni = self.search_dni_input.text()

        doctor = self._controller.search_by_dni(dni)

        if doctor:
            # doctor.dni -> llama al getter
            # doctor.hospital.nombre -> llama al getter de hospital, y luego al de nombre
            self.tabla_resultados.setRowCount(1)
            self.tabla_resultados.setItem(0, 0, QTableWidgetItem(doctor.dni))
            self.tabla_resultados.setItem(0, 1, QTableWidgetItem(doctor.nombre))
            self.tabla_resultados.setItem(0, 2, QTableWidgetItem(doctor.especialidad))
            self.tabla_resultados.setItem(0, 3, QTableWidgetItem(doctor.hospital.nombre))
        else:
            # Limpiamos la tabla si no hay resultados
            self.tabla_resultados.setRowCount(0)
            self.mostrar_dialogo("No Encontrado",
                                 f"No se encontró ningún doctor con el DNI {dni}.",
                                 "info")

    def mostrar_dialogo(self, titulo: str, mensaje: str, tipo: str = "info"):
        """
        Función helper para mostrar el diálogo de feedback personalizado.
        """
        dialogo = OutputWindow(self)

        dialogo.set_message(titulo, mensaje, tipo)

        dialogo.exec()