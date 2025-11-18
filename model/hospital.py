class Hospital:
    """
    Representa a una entidad hospitalaria.
    Usa propiedades para encapsular el acceso a los atributos.
    """

    def __init__(self, nombre: str):
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    def __str__(self) -> str:
        return f"Hospital {self.nombre}"