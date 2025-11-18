from model.hospital import Hospital
from model.doctor import Doctor
from typing import Dict, Optional, Tuple


class HospitalController:
    """
    Controla toda la lógica de la aplicación, actuando como
    intermediario entre la Vista (GUI) y el Modelo (datos).
    """

    def __init__(self):
        """
        Inicializa el controlador.
        Simulamos la persistencia de datos con atributos privados.
        """
        self._hospital: Optional[Hospital] = None
        # Usamos un diccionario para búsqueda rápida por DNI (simula una BD)
        self._doctores_repo: Dict[str, Doctor] = {}

    def crear_hospital(self, nombre_hospital: str) -> Tuple[bool, str]:
        """
        Crea o actualiza la instancia principal del hospital.

        Devuelve:
            Tuple[bool, str]: (éxito, mensaje_de_feedback)
        """
        if not nombre_hospital.strip():
            return False, "Error: El nombre del hospital no puede estar vacío."

        self._hospital = Hospital(nombre_hospital)
        return True, f"Hospital '{self._hospital.nombre}' establecido con éxito."

    def agregar_doctor(self, dni: str, nombre: str, especialidad: str) -> Tuple[bool, str]:
        """
        Valida y agrega un nuevo doctor al sistema.

        Devuelve:
            Tuple[bool, str]: (éxito, mensaje_de_feedback)
        """
        # 1. Validación de estado (POO - Invariantes)
        if not self._hospital:
            return False, "Error: Primero debe establecer el nombre del hospital."

        # 2. Validación de entradas
        if not dni.strip() or not nombre.strip() or not especialidad.strip():
            return False, "Error: Todos los campos del doctor son obligatorios."

        if not dni.isdigit():
            return False, "Error: El DNI solo debe contener números."

        # 3. Regla de negocio (No duplicados)
        if dni in self._doctores_repo:
            return False, "Error: Ya existe un doctor registrado con ese DNI."

        # 4. Lógica de negocio (Creación y almacenamiento)
        try:
            nuevo_doctor = Doctor(dni, nombre, especialidad)

            # AUNQUE PARECE ACCESO DIRECTO, ¡ESTO LLAMA AL SETTER!
            # nuevo_doctor.hospital = ... -> Llama a @hospital.setter
            nuevo_doctor.hospital = self._hospital

            self._doctores_repo[dni] = nuevo_doctor
            return True, "Doctor agregado exitosamente."

        except Exception as e:
            return False, f"Error inesperado al guardar: {str(e)}"

    def search_by_dni(self, dni: str) -> Optional[Doctor]:
        """
        Implementa la función search_by_dni() requerida.

        Devuelve el objeto Doctor si se encuentra, o None.
        """
        if not dni.strip():
            return None

        return self._doctores_repo.get(dni)