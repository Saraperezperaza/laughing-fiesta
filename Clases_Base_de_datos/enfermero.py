from trabajador import Trabajador
class Enfermero(Trabajador):
    """
    Clase que representa a un enfermero del sistema hospitalario. Hereda de la clase Trabajador y añade
    atributos y comportamientos específicos como especialidad, antigüedad, cálculo de salario y gestión de pacientes.


    Parámetros
    ----------
    id : str
        Identificador del enfermero. Debe comenzar por 'ENF'.
    nombre : str
        Nombre del enfermero.
    apellido : str
        Apellido del enfermero.
    edad : int
        Edad del enfermero.
    genero : str
        Género del enfermero.
    turno : str
        Turno de trabajo del enfermero ('mañana', 'tarde' o 'noche').
    horas : int
        Cantidad de horas trabajadas por semana.
    salario : float
        Salario base del enfermero.
    especialidad : str
        Especialidad del enfermero.
    antiguedad : int
        Años de experiencia o servicio.
    username : str
        Nombre de usuario para el sistema.
    password : str
        Contraseña para el sistema.

    Excepciones
    -----------
    ValueError
        Si el ID no comienza con 'ENF'.
    """

    def __init__(self, id: str, nombre: str, apellido: str, edad: int, genero: str,
                 turno: str, horas: int, salario: float, especialidad: str,
                 antiguedad: int, username: str, password: str):
        super().__init__(id, nombre, apellido, edad, genero, turno, horas, salario)
        self.especialidad = especialidad
        self.antiguedad = antiguedad
        self._salario = self.calculo_salario()
        self.auxiliar_asignado = None
        self.pacientes_asignados = []
        self.username = username
        self.__password = password
        self.rol = 'enfermero'
        if not id.startswith('ENF'):
            raise ValueError('ID inválido, el ID debe empezar por ENF')

    def asignar_auxiliar(self, auxiliar: object)->None:
            self.auxiliar_asignado = auxiliar #Asignar 1 auxiliar a 1 enfermero

    def calculo_salario(self) -> float:
        """
        Calcula el salario final del enfermero en función de la antigüedad y el turno.

        Devuelve
        --------
        float
        Salario actualizado del enfermero.
        """
        nuevo_salario = self._salario
        if self.antiguedad <= 2:
            nuevo_salario = self._salario
        elif 2 < self.antiguedad <= 7:
            nuevo_salario = 0.15 * self._salario + self._salario
        elif 7 < self.antiguedad <= 12:
            nuevo_salario = 0.2 * self._salario + self._salario
        elif self.antiguedad > 12:
            nuevo_salario = self._salario * 0.3 + self._salario
        if self.turno.lower() == 'noche':
            nuevo_salario = nuevo_salario * 0.15 + nuevo_salario
        return nuevo_salario

    def asignar_paciente(self, paciente) -> None:
        """
        Asigna un paciente al enfermero si aún no tiene uno asignado.

        Parámetros
        ----------
        paciente : Paciente
        Instancia de la clase Paciente que será asignada.

        Excepciones
        -----------
        ValueError
            Si el paciente ya tiene un enfermero asignado.
        """
        if paciente.enfermero_asignado is not None: #Si el paciente ya tiene enfermero salta ValueError
            raise ValueError(f'El paciente {paciente.nombre} ya tiene un enfermero asignado.')
        else: #Si no, añadimos el paciente a la lista de pacientes asignados a 1 enfermero
            self.pacientes_asignados.append(paciente)
            paciente.asignar_enfermero(self)

    def mostrar_pacientes(self):
        """
        Genera una cadena con la información de los pacientes asignados al enfermero.
        Devuelve
        --------
            str
        Lista formateada de pacientes o un mensaje indicando que no hay pacientes asignados.
        """
        if not self.pacientes_asignados:
            return 'No hay pacientes asignados'
        else:
            pacientes_info = 'Pacientes asignados: '
            for paciente in self.pacientes_asignados:
                pacientes_info += f'Nombre: {paciente.nombre} - Apellido: {paciente.apellido} - ID: {paciente.id}, '
            return pacientes_info.rstrip(', ')


    def to_dict(self) -> dict:
        """
        Convierte el objeto Enfermero a un diccionario con sus atributos principales.

        Devuelve
        --------
            dict
        Diccionario representando el estado del objeto.
        """
        lista_ids = []
        for paciente in self.pacientes_asignados:
            lista_ids.append(paciente.id)
        return {
            'id': self.id,
            'nombre': self._nombre,
            'apellido': self._apellido,
            'edad': self.edad,
            'genero': self._genero,
            'turno': self.turno,
            'horas': self.horas,
            'salario': self._salario,
            'especialidad': self.especialidad,
            'antiguedad': self.antiguedad,
            'username': self.username,
            'password': self.__password,
            'rol': self.rol,
            'pacientes_asignados': lista_ids
        }

    def __str__(self) -> str:
        """
        Representación en forma de cadena del enfermero.

        Devuelve
        --------
            str
        Cadena con los atributos más relevantes del enfermero.
        """
        return (f'ID: {self.id} - Nombre: {self._nombre} - Apellido: {self._apellido} - Edad: {self.edad} - Género: {self._genero} - Turno: {self.turno} '
                    f'- Horas: {self.horas} - Especialidad: {self.especialidad} - Salario: {self._salario} - Antiguedad: {self.antiguedad}')
