from abc import ABC, abstractmethod
class Comunidad(ABC):
    """
    Clase abstracta `Comunidad`, que representa una comunidad con un nombre y un presupuesto.
    Esta clase es una plantilla para crear comunidades y no se pueden crear objetos directamente de ella.

    Atributos
    ----------
    nombre_comunidad : str
        Nombre de la comunidad.
    presupuesto : float
        Presupuesto asignado a la comunidad. Inicializado a 0.

    Métodos
    -------
    obtener_info() :
        Devuelve la información básica sobre la comunidad (nombre y presupuesto).

    asignar_presupuesto(cantidad) :
        Asigna una cantidad al presupuesto de la comunidad, validando que no sea negativa.
        Si la cantidad es negativa, se lanza una excepción `ValueError`.
    """

    def __init__(self, nombre_comunidad: str):
        """
        Inicializa una instancia de `Comunidad`.

        Parámetros
        ----------
        nombre_comunidad : str
            Nombre de la comunidad.
        """
        self.nombre_comunidad = nombre_comunidad
        self.presupuesto = 0  # El presupuesto inicial es 0.
    def obtener_info(self) -> str:
        """
        Devuelve la información básica sobre la comunidad.

        Devuelve
        -------
        str
            Información sobre el nombre de la comunidad y su presupuesto.
        """
        return f'Nombre: {self.nombre_comunidad} - Presupuesto: {self.presupuesto}'
    @abstractmethod
    def asignar_presupuesto(self, cantidad: float) -> str:
        """
        Asigna un presupuesto a la comunidad, validando que no sea negativa.

        Parámetros
        ----------
        cantidad : float
            La cantidad que se desea agregar al presupuesto de la comunidad.

        Devuelve
        -------
        str
            Mensaje confirmando el nuevo presupuesto de la comunidad.

        Excepciones
        ------------
        ValueError
            Si la cantidad proporcionada es negativa.
        """
        if cantidad < 0:
            raise ValueError('No se admiten presupuestos negativos')
        else:
            self.presupuesto += cantidad
            return f'Nuevo presupuesto para {self.nombre_comunidad}: {self.presupuesto}€'
        #No se crean objetos porque se trata de una clase abstracta