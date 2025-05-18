from Clases_Base_de_datos.trabajador import Trabajador

class Paramedico(Trabajador):
    """
    Clase que representa a un paramédico dentro del sistema hospitalario. Hereda de la clase Trabajador
    y extiende con atributos específicos como especialidad, antigüedad y ambulancia asignada.

    Atributos
    ----------
    id : str
        Identificador único del paramédico.
    nombre : str
        Nombre del paramédico.
    apellido : str
        Apellido del paramédico.
    edad : int
        Edad del paramédico.
    genero : str
        Género del paramédico.
    turno : str
        Turno de trabajo del paramédico (mañana, tarde, noche).
    horas : int
        Número de horas de trabajo semanales del paramédico.
    salario : float
        Salario del paramédico.
    especialidad : str
        Especialidad del paramédico (por ejemplo, Emergencias, Cardiología, etc.).
    antiguedad : int
        Antigüedad del paramédico en años.
    ambulancia_asignada : Ambulancia, opcional
        Ambulancia asignada al paramédico. Por defecto es None.

    Métodos
    -------
    __init__(id: str, nombre: str, apellido: str, edad: int, genero: str, turno: str, horas: int, salario: float, especialidad: str, antiguedad: int)
        Inicializa los atributos del paramédico, incluyendo validación del id.

    asignar_ambulancia(ambulancia: Ambulancia) -> None
        Asigna una ambulancia al paramédico, asegurándose de que no esté asignado a otra.

    __str__() -> str
        Retorna una cadena con los detalles del paramédico, incluyendo la ambulancia asignada si la tiene.
    """

    def __init__(self, id: str, nombre: str, apellido: str, edad: int, genero: str, turno: str, horas: int,
                 salario: float, especialidad: str, antiguedad: int) -> None:
        """
        Inicializa los atributos del paramédico, asegurándose de que el id comience con 'PAR'.

        Parámetros
        ----------
        id : str
            Identificador único del paramédico.
        nombre : str
            Nombre del paramédico.
        apellido : str
            Apellido del paramédico.
        edad : int
            Edad del paramédico.
        genero : str
            Género del paramédico.
        turno : str
            Turno de trabajo del paramédico (mañana, tarde, noche).
        horas : int
            Número de horas de trabajo semanales del paramédico.
        salario : float
            Salario del paramédico.
        especialidad : str
            Especialidad del paramédico (por ejemplo, Emergencias, Cardiología, etc.).
        antiguedad : int
            Antigüedad del paramédico en años.

        Excepciones
        ------------
        ValueError
            Si el id no empieza con 'PAR'.
        """
        super().__init__(id, nombre, apellido, edad, genero, turno, horas, salario)
        self.especialidad = especialidad
        self.antiguedad = antiguedad
        if not id.startswith('PAR'): #Si el id no empieza por PAR salta el error
            raise ValueError('Has insertado un id inválido, debe empezar por PAR')

    def __str__(self) -> str:
        """
        Devuelve una cadena con los detalles del paramédico.

        Devuelve
        -------
        str
            Información detallada sobre el paramédico.
        """
        return (
            f'Nombre: {self.nombre} - ID: {self.id} - Edad: {self.edad} - Género: {self._genero} - Turno: {self.turno} - Horas: {self.horas} - '
            f' Salario: {self._salario} - Especialidad: {self.especialidad} - Antiguedad: {self.antiguedad} ')
