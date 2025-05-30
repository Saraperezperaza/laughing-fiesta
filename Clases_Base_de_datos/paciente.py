from typing import List
from Clases_Base_de_datos.persona import Persona
class Paciente(Persona):
    """
    Clase que representa a un paciente en el sistema de gestión hospitalaria.

    Atributos
    ---------
    id : str
        Identificador único del paciente.
    username : str
        Nombre de usuario del paciente.
    password : str
        Contraseña del paciente.
    nombre : str
        Nombre del paciente.
    apellido : str
        Apellido del paciente.
    edad : int
        Edad del paciente.
    genero : str
        Género del paciente.
    estado : str
        Estado actual del paciente (grave, moderado, leve).
    medico_asignado : Medico, opcional
        Médico asignado al paciente.
    enfermero_asignado : Enfermero, opcional
        Enfermero asignado al paciente.
    habitacion_asginada : Habitacion, opcional
        Habitación asignada al paciente.
    enfermedades : List[str]
        Lista de enfermedades diagnosticadas al paciente.
    prioridad_urgencias : int
        Prioridad del paciente en urgencias (1: alta, 2: moderada, 3: baja).
    historial_medico : List[str]
        Historial médico del paciente.
    citas : List[Cita]
        Lista de citas del paciente.

    Métodos
    -------
    asignar_medico(medico: Medico) -> str
        Asigna un médico al paciente y devuelve un mensaje confirmando la asignación.

    asignar_habitacion(habitacion: Habitacion) -> str
        Asigna una habitación al paciente y devuelve un mensaje confirmando la asignación.

    asignar_enfermero(enfermero: Enfermero) -> str
        Asigna un enfermero al paciente y devuelve un mensaje confirmando la asignación.

    cambiar_estado(nuevo_estado: str) -> None
        Cambia el estado del paciente a un nuevo valor (grave, moderado, leve).

    prioridad_urgencias() -> None
        Establece la prioridad del paciente en urgencias según su estado (grave, moderado, leve).

    asignar_enfermedades(enfermedad: str) -> None
        Asigna una enfermedad al paciente si no está ya registrada en su historial.

    to_dict() -> dict
        Devuelve un diccionario con los atributos del paciente.
    """

    def __init__(self, id: str,username: str, password: str, nombre: str, apellido: str, edad: int, genero: str, estado: str, historial_medico: List[str] = None):
        super().__init__(id, nombre, apellido, edad, genero, 'paciente', password)
        from Clases_Base_de_datos.citas import Cita
        self.username = username
        self.__password = password
        self.estado = estado
        self.enfermedades = []
        self.alergias = []
        self._prioridad_urgencias = 0
        if historial_medico is not None: #Es opcional, si se inserta algo se guarda en el historial, sino, es una lista vacía
            self.historial_medico = historial_medico
        else:
            self.historial_medico = []
        self.citas: List[Cita] = []

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """
        Cambia el estado del paciente a un nuevo valor (grave, moderado, leve).

        Parámetros
        ----------
        nuevo_estado : str
            Nuevo estado del paciente.
        """
        self.estado = nuevo_estado

    def prioridad_urgencias(self)-> None:
        """
        Establece la prioridad del paciente en urgencias según su estado (grave, moderado, leve).

        Devuelve
        --------
        None
            Modifica el valor de prioridad_urgencias en función del estado del paciente.
        """
        if self.estado.lower() == 'grave':
            self._prioridad_urgencias = 1
            print(f'El paciente {self.nombre} tiene prioridad alta en urgencias.')
        elif self.estado.lower() == 'moderado':
            self._prioridad_urgencias = 2
            print(f'El paciente {self.nombre} tiene prioridad moderada en urgencias.')
        elif self.estado.lower() == 'leve':
            self._prioridad_urgencias = 3
            print(f'El paciente {self.nombre} tiene prioridad baja en urgencias.')

    def asignar_enfermedades(self, enfermedad: object) -> None:
        """
        Asigna una enfermedad al paciente si aún no la tiene registrada.

        Parámetros
        ----------
        enfermedad : Enfermedad
            Objeto de tipo Enfermedad que se desea asignar al paciente.

        Devuelve
        --------
        None
            No retorna valor. Modifica internamente la lista de enfermedades del paciente
            y muestra un mensaje indicando si fue asignada o ya existía.
        """
        if enfermedad not in self.enfermedades:
            self.enfermedades.append(enfermedad)
            print(f'Se ha asignado la enfermedad al paciente {self.nombre}.')
        else:
            print(f'El paciente {self.nombre} ya tiene registrada la enfermedad')

    def to_dict(self)->dict:
        """
        Devuelve un diccionario con los atributos del paciente.

        Devuelve
        --------
        dict
            Diccionario con los atributos del paciente, incluyendo médicos, enfermeros, habitación y citas.
        """
        lista_citas = []
        for cita in self.citas:
            lista_citas.append(cita.to_dict()) #Añadimos todas las citas a la lista de citas
        return {
            'id': self.id,
            'username': self.username,
            'password': self.__password,
            'nombre': self.nombre,
            'edad': self.edad,
            'historial_medico': self.historial_medico,
            'citas': lista_citas,
            'rol': self._rol,
            'estado': self.estado,
        }