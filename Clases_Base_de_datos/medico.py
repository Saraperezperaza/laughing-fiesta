from trabajador import Trabajador

class Medico(Trabajador):
    """
    Representa a un médico del sistema sanitario.

    Hereda de
    ---------
    Trabajador

    Atributos
    ---------
    username : str
        Nombre de usuario para el acceso del médico.
    password : str
        Contraseña asociada al usuario.
    especialidad : str
        Área médica en la que está especializado el médico.
    antiguedad : int
        Años de experiencia del médico.
    pacientes_asignados : list
        Lista de objetos de tipo Paciente asignados a este médico.
    salario : float
        Salario ajustado en base a antigüedad y turno.
    """

    def __init__(self, id: str, username: str, password: str, nombre: str, apellido: str, edad: int, genero: str,
                     turno: str, horas: int, salario: float, especialidad: str, antiguedad: int)->None:
        """
        Inicializa un objeto Medico con los datos proporcionados y ajusta el salario según la experiencia.

        Parámetros
        ----------
        id : str
            Identificador único del médico, debe comenzar por 'MED'.
        username : str
            Nombre de usuario para el acceso del médico.
        password : str
            Contraseña de acceso.
        nombre : str
            Nombre del médico.
        apellido : str
            Apellido del médico.
        edad : int
            Edad del médico.
        genero : str
            Género del médico.
        turno : str
            Turno de trabajo ('mañana', 'tarde', 'noche').
        horas : int
            Número de horas trabajadas semanalmente.
        salario : float
            Salario base del médico.
        especialidad : str
            Especialidad médica del profesional.
        antiguedad : int
            Años de experiencia laboral en el sector.

        Excepciones
        -----------
        ValueError
            Si el ID no comienza por 'MED'.
    """
        super().__init__(id, nombre, apellido, edad, genero, turno, horas)
        self.username = username
        self.__password = password
        self.especialidad = especialidad
        self.antiguedad = antiguedad
        self._salario = salario
        self._salario = self.calculo_salario()
        if not id.startswith('MED'):
            raise ValueError('ID inválido, el ID debe empezar por MED')
    def calculo_salario(self) -> float:
        """
        Calcula el salario ajustado del médico en base a su antigüedad y turno.

        Devuelve
        --------
        float
            Salario ajustado del médico.
        """
        salario_base = self._salario
        if self.antiguedad <= 1:
            nuevo_salario = salario_base
        elif self.antiguedad <= 5: #El salario aumenta en cierto porcentaje dependiendo de los años de antiguedad
            nuevo_salario = 0.2 * salario_base + salario_base
        elif self.antiguedad <= 10:
            nuevo_salario = 0.3 * salario_base + salario_base
        else:
            nuevo_salario = 0.5 * self._salario + self._salario
        if self.turno.lower() == 'noche': #Hay bonificación en el salario por turno de noche
            nuevo_salario = nuevo_salario * 0.2 + nuevo_salario
        return nuevo_salario

    def to_dict(self) -> dict:
        """
        Convierte la información del médico en un diccionario.

        Devuelve
        --------
        dict
            Diccionario con los atributos clave del médico.
        """
        return {
            'id': self.id,
            'username': self.username,
            'password': self.__password,
            'nombre': self._nombre,
            'apellido': self._apellido,
            'edad': self.edad,
            'genero': self._genero,
            'horas': self.horas,
            'especialidad': self.especialidad,
            'antiguedad': self.antiguedad,
            'turno': self.turno.lower(),
            'rol': self._rol,
            'salario': self._salario
        }

    def __str__(self) -> str:
        """
        Devuelve una representación en texto del objeto médico.

        Devuelve
        --------
        str
            Representación en texto del médico.
        """
        return (
            f'ID: {self.id} - Nombre: {self._nombre} - Apellido {self._apellido} - Edad {self.edad} - Género {self._genero} - Turno: {self.turno} - '
            f'Horas: {self.horas} - Especialidad: {self.especialidad} - Salario: {self._salario} - Antiguedad: {self.antiguedad}'
        )

