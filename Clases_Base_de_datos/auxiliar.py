from trabajador import Trabajador

class Auxiliar(Trabajador):
    """
    Clase que representa un auxiliar en el sistema hospitalario.
    Hereda de la clase `Trabajador`.

    Atributos
    ----------
    id : str
        Identificador único del auxiliar. Debe empezar por 'AUX'.
    nombre : str
        Nombre del auxiliar.
    apellido : str
        Apellido del auxiliar.
    edad : int
        Edad del auxiliar.
    genero : str
        Género del auxiliar.
    turno : str
        Turno asignado al auxiliar (mañana, tarde, noche).
    horas : int
        Número de horas trabajadas semanalmente.
    salario : float
        Salario base del auxiliar, ajustado según antigüedad y turno.
    enfermero_asignado : object or None
        Enfermero asignado al auxiliar. Puede ser un objeto de la clase `Enfermero`.
    antiguedad : int
        Antigüedad del auxiliar en años.

    Métodos
    -------
    __init__(self, id, nombre, apellido, edad, genero, turno, horas, salario, enfermero_asignado, antiguedad)
        Inicializa una nueva instancia de `Auxiliar`.

    calculo_salario(self) -> float
        Calcula y devuelve el salario del auxiliar según su antigüedad y turno.

    limpiar_habitacion(self, habitaciones) -> list
        Limpia las habitaciones que no están limpias y devuelve una lista de las habitaciones que han sido limpiadas.

    asignar_enfermero(self, enfermero) -> None
        Asigna un enfermero al auxiliar, si no tiene uno asignado.
    """

    def __init__(self, id: str, nombre: str, apellido: str, edad: int, genero: str, turno: str, horas: int, salario: float, antiguedad: int, id_enfermero: str) -> None:
        """
        Inicializa una instancia de `Auxiliar`. Valida el ID, ajusta el salario y asigna los atributos.

        Parámetros
        ----------
        id : str
            Identificador único del auxiliar. Debe comenzar con 'AUX'.
        nombre : str
            Nombre del auxiliar.
        apellido : str
            Apellido del auxiliar.
        edad : int
            Edad del auxiliar.
        genero : str
            Género del auxiliar.
        turno : str
            Turno de trabajo asignado (mañana, tarde, noche).
        horas : int
            Número de horas trabajadas semanalmente.
        salario : float
            Salario base del auxiliar.
        enfermero_asignado : object or None
            Instancia de un enfermero asignado al auxiliar.
        antiguedad : int
            Antigüedad en años del auxiliar.

        Excepciones
        ------
        ValueError
            Si el ID no empieza por 'AUX'.
        """
        super().__init__(id, nombre, apellido, edad, genero, turno, horas, salario)
        self.antiguedad = antiguedad
        if not id.startswith('AUX'):
            raise ValueError('ID inválido, el ID debe empezar por AUX')
        self.salario = self.calculo_salario()
        self.id_enfermero = id_enfermero

    def calculo_salario(self) -> float:
        """
        Calcula el salario del auxiliar en función de su antigüedad y turno de trabajo.

        Devuelve
        -------
        float
            El salario ajustado del auxiliar.
        """
        nuevo_salario = self.salario
        if self.antiguedad <= 2:
            nuevo_salario = self.salario
        elif self.antiguedad > 2 and self.antiguedad <= 7:
            nuevo_salario = 0.10 * self.salario + self.salario
        elif self.antiguedad > 7 and self.antiguedad <= 12:
            nuevo_salario = 0.15 * self.salario + self.salario
        elif self.antiguedad > 12:
            nuevo_salario = self.salario * 0.25 + self.salario
        if self.turno.lower() == 'noche':
            nuevo_salario = nuevo_salario * 0.10 + nuevo_salario
        return nuevo_salario  # Devuelve el salario ajustado

    def limpiar_habitacion(self, habitaciones: list) -> list:
        """
        Limpia las habitaciones que no están limpias y devuelve una lista de las habitaciones que han sido limpiadas.

        Parámetros
        ----------
        habitaciones : list
            Lista de objetos `Habitacion` que el auxiliar debe limpiar.

        Devuelve
        -------
        list
            Lista de habitaciones que fueron limpiadas.
        """
        habitaciones_limpiadas = []
        for habitacion in habitaciones:
            if not habitacion.limpia:
                habitacion.limpia = True
                print(f'La habitación {habitacion.numero} ha sido limpiada, nuevo estado de la habitación:')
                habitaciones_limpiadas.append(habitacion)
            else:
                print(f'La habitación {habitacion.numero} ya está limpia')
        return habitaciones_limpiadas  # Devuelve la lista de habitaciones limpiadas
