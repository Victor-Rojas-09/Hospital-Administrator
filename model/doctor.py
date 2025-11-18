from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hospital import Hospital


class Doctor:
    """
    Representa a un doctor.
    Usa propiedades para encapsular el acceso a los atributos.
    """

    def __init__(self, dni: str, nombre: str, especialidad: str):
        self._dni = dni
        self._nombre = nombre
        self._especialidad = especialidad
        self._hospital: 'Hospital' | None = None

    @property
    def dni(self) -> str:
        return self._dni

    @dni.setter
    def dni(self, value: str):
        self._dni = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, value: str):
        self._especialidad = value

    @property
    def hospital(self) -> 'Hospital' | None:
        return self._hospital

    @hospital.setter
    def hospital(self, value: 'Hospital' | None):
        self._hospital = value

    def __str__(self) -> str:
        return f"Dr. {self.nombre} (DNI: {self.dni}), {self.especialidad}"