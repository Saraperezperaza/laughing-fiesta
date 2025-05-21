from typing import List
from Clases_Base_de_datos.citas import Cita
from Clases_Base_de_datos.paciente import Paciente

class CitaPresencial(Cita):

    """ Clase que hereada directamente de la clase abstracta Cita dentro de
    nuestra base de datos """

    def __init__(self, id_cita: str, paciente: Paciente, medico : str, fecha_hora_dt, centro: str):

        """ Parámetros:
            -----------
             - Id_cita -> Id unico que identifica cada cita pedida
             - Paciente -> El paciente que pide o recibe esta cita
             - medico -> Medico asociado a dicha cita
             - fecha -> Fecha de la cita
             - hora -> Hora de la cita
             - centro -> Centro de la cita
        """

        super().__init__(id_cita, paciente, medico, fecha_hora_dt)
        self.centro = centro

    def cancelar_cita(self) -> str:
        self.estado = 'Cancelada'
        return f'La cita presencial {self.id_cita} el dia {self.fecha_hora_dt} en el centro{self.centro} y ha sido cancelada'

    def ser_atendido(self):
        self.atendido = True
        return f'El paciente esta siendo atendido'


class CitaTelefonica(Cita):

    """ Clase que hereda directamente de la clase abstracta Cita dentro de la base de datos creada"""

    def __init__(self, id_cita: str, paciente: Paciente, medico: str, fecha_hora_dt, telefono_contacto: str):

        """ Parametros:
            -----------
             - Id_cita -> Id unico que identifica cada cita pedida
             - Paciente -> El paciente que pide o recibe esta cita
             - medico -> Medico asociado a dicha cita
             - fecha -> Fecha de la cita
             - hora -> Hora de la cita
             - telefono_contacto -> Telefono de contacto para la llamada

        """
        super().__init__(id_cita, paciente, medico, fecha_hora_dt)
        self.telefono_contacto = telefono_contacto

    def cancelar_cita(self) -> str:
        self.estado = 'Cancelada'
        self.atendido = False
        return f'La cita telefónica {self.id_cita} ha sido cancelada'

    def ser_atendido(self):
        self.atendido = True
        return f'El paciente esta siendo atendido por teléfono al {self.telefono_contacto}'


class CitaUrgencias(Cita):

    """ Esta nueva clase vuelve a heredar de la clase base Cita (creada en la base de datos)
    pero en este caso se representan las citas de urgencias dentro del hospital """

    def __init__(self, id_cita: str, paciente: Paciente, medico: str, fecha_hora_dt, nivel_prioridad: str):

        """ Parametros:
            -----------
             - Id_cita -> Id unico que identifica cada cita pedida
             - Paciente -> El paciente que pide o recibe esta cita
             - medico -> Medico asociado a dicha cita
             - fecha -> Fecha de la cita
             - hora -> Hora de la cita
             - nivel_prioridad -> Nivel de la urgencia
             """
        super().__init__(id_cita, paciente, medico, fecha_hora_dt)
        self.nivel_prioridad = nivel_prioridad

    def cancelar_cita(self) -> str:
        self.estado = 'Cancelada'
        self.atendido = False
        return f'La cita de urgencia ha sido cancelada'

    def ser_atendido(self):
        self.atendido = True
        return f'El paciente esta siendo atendido de urgencia debido a que su prioridad es {self.nivel_prioridad}'


class GestorCitas:

    """
        Gestiona la creación, almacenamiento y control de citas médicas.
        """

    def __init__(self):
        """
        Inicializa un nuevo gestor de citas.

        Atributos:
        -----------
        lista_citas : List[Cita]
            Lista que almacena las citas médicas creadas. Cada objeto de cita debe contener:
                - id_cita: Id único que identifica cada cita pedida.
                - paciente: El paciente que pide o recibe la cita.
                - medico: Médico asociado a dicha cita.
                - fecha: Fecha de la cita.
                - hora: Hora de la cita.
                DEPENDIENDO DE LA CITA:
                - centro -> Centro de la cita
                - telefono_contacto -> Telefono de contacto para la llamada
                - nivel_prioridad: Nivel de la urgencia (aplicable a citas de urgencias).
        """

        self.lista_citas: List[Cita] = []

    def anadir_cita(self, cita:Cita) -> None:

        """ Añade una nueva cita"""

        self.lista_citas.append(cita)

    def cancelar_cita(self, id_cita : int) -> str:

        """ Cancela una cita dependiendo de su ID """

        for cita in self.lista_citas:
            if cita.id_cita == id_cita:
                return cita.cancelar_cita()
        return 'Cita no encontrada'

    def atender_cita(self, id_cita: int) -> str:

        """ Marca que una cita ha sido atentdida dependiendo de su id"""

        for cita in self.lista_citas:
            if cita.id_cita == id_cita:
                return f'La cita ha sido atendida'
        return 'Cita no encontrada'

    def mostrar_citas(self) -> None:

        """ Muestra todas las citas """

        for cita in self.lista_citas:
            if cita.atendido:
                estado = "Atendido"
            else:
                estado = "Pendiente"

            print(f'{cita.id_cita} - {cita.__class__.__name__} - Paciente: {cita.paciente} - Médico: {cita.medico} - {estado}')

    def __iadd__(self, cita:Cita):

        """
            Sobrecarga del operador += para añdir una cita al gestor.
            Permite usar : gestor += cita
        """

        self.anadir_cita(cita)
        return self
