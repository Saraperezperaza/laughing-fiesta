from abc import ABC, abstractmethod
from datetime import datetime

class Cita(ABC):
    """
    Clase abstracta que representa una cita médica. Los atributos de esta clase incluyen el ID de la cita,
    el paciente, el médico, la fecha y la hora de la cita, el estado (pendiente, cancelado, completado)
    y si la cita ha sido atendida o no. Esta clase es una plantilla para crear objetos de citas médicas
    y debe ser heredada para ser utilizada.

    Atributos
    ---------
    id_cita : str
        Identificador único de la cita.
    paciente : str
        Nombre del paciente.
    medico : str
        Nombre del médico asignado.
    Fecha_hora : str
        Fehca y hora en la que se llevará a cabo la cita.
    estado : str, opcional
        Estado de la cita. Por defecto es 'pendiente'.
    atendido : bool, opcional
        Si la cita ha sido atendida o no. Por defecto es False.

    Métodos
    --------
    __init__(self, id_cita, paciente, medico, fecha_hora, estado='pendiente', atendido=False)
        Inicializa una nueva cita médica con el ID, paciente, médico, fecha_hora, estado y si ha sido atendida o no.

    cancelar_cita(self)
        Cancela la cita, cambia el estado a 'cancelado' y marca la cita como no atendida.

    ser_atendido(self)
        Marca la cita como atendida y cambia su estado a 'completado'.
    """
    def __init__(self, id_cita: str, paciente: str, medico: str, fecha_hora: str, motivo: str = '',  estado: str='pendiente', atendido: bool=False) -> None:
        """
        Inicializa una nueva cita médica con el ID, paciente, médico, fecha_hora, estado y si ha sido atendida o no.

        Parámetros
        ----------
        id_cita : str
            Identificador único de la cita.
        paciente : str
            Nombre del paciente.
        medico : str
            Nombre del médico asignado.
        fecha_hora : str
            Fecha y hora en la que se llevará a cabo la cita.
        estado : str, opcional
            Estado de la cita, por defecto 'pendiente'.
        atendido : bool, opcional
            Si la cita ha sido atendida o no, por defecto False.
        """
        self.id_cita = id_cita
        self.paciente = paciente
        self.medico = medico
        self.motivo = motivo
        self.fecha_hora_dt = datetime.strptime(fecha_hora, '%Y %m %d %H:%M')
        self.estado = estado
        self.atendido = atendido

    @abstractmethod
    def cancelar_cita(self) -> str:
        """
        Cancela la cita médica, cambia el estado a 'cancelado' y marca la cita como no atendida.

        Devuelve
        -------
        str
            Mensaje indicando que la cita ha sido cancelada.
        """
        self.estado = 'cancelado'
        self.atendido = False
        return f'El paciente {self.paciente} ha cancelado la cita {self.id_cita}'

    @abstractmethod
    def ser_atendido(self)-> bool:
        """
        Marca la cita como atendida, cambia el estado a 'completado'.

        Devuelve
        -------
        bool
            Devuelve True para indicar que la cita ha sido atendida.
        """
        # Cambiar el estado de la cita y marcarla como atendida
        self.atendido = True
        self.estado = 'completado'
        return self.atendido

    def se_solapa(self, otra_cita: 'Cita') -> bool:
        """
        Determina si esta cita se solapa con otra cita (menos de 30 minutos de diferencia).

        Parámetros
        ----------
        otra_cita : Cita
            Otra cita con la que se quiere comprobar el solapamiento.

        Devuelve
        --------
        bool
            True si las citas se solapan, False en caso contrario.
        """
        delta = abs((self.fecha_hora_dt - otra_cita.fecha_hora_dt).total_seconds())
        return delta < 1800

    def to_dict(self) -> dict:
        """
        Devuelve una representación de la cita como diccionario.

        Devuelve
        --------
        dict
            Diccionario con los datos de la cita.
        """
        return {
            'id_cita': self.id_cita,
            'paciente': self.paciente,
            'medico': self.medico,
            'motivo': self.motivo,
            'fecha_hora': self.fecha_hora_dt.strftime('%Y-%m-%d %H:%M'),
            'estado': self.estado,
            'atendido': self.atendido
        }
#Como cita es una clase abstracta, no se pueden crear objetos