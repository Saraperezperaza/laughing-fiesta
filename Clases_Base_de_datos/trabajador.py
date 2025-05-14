from persona import Persona

class Trabajador(Persona):
    """
    Clase que representa a un trabajador del sistema hospitalario, heredando de Persona.
    Contiene información sobre su turno, horas diarias y salario mensual.
    """

    def __init__(self, id: str, nombre: str, apellido: str, edad: int, genero: str, turno: str, horas: int, salario: float = 0.0, password: str = "default_password"):
        """
        Inicializa los atributos del trabajador.

        Parámetros
        ----------
        id : str
            Identificador único del trabajador.
        nombre : str
            Nombre del trabajador.
        apellido : str
            Apellido del trabajador.
        edad : int
            Edad del trabajador.
        genero : str
            Género del trabajador.
        turno : str
            Turno de trabajo (mañana, tarde, noche).
        horas : int
            Número de horas que trabaja al día.
        salario : float, opcional
            Salario mensual del trabajador. Por defecto es 0.0.
        password : str, opcional
            Contraseña del trabajador. Por defecto es "default_password".
        """
        if not isinstance(id, str) or not id.strip(): #Si id no es una cadena o esta vacía, salta el error
            raise ValueError("El ID debe ser una cadena no vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        if not isinstance(apellido, str) or not apellido.strip():
            raise ValueError("El apellido debe ser una cadena no vacía.")
        if not isinstance(edad, int) or edad <= 0: #Si edad no es un entero o es menor o igual a 0 salta el error
            raise ValueError("La edad debe ser un entero positivo.")
        if not isinstance(genero, str) or not genero.strip():
            raise ValueError("El género debe ser una cadena no vacía.")
        if not isinstance(turno, str) or not turno.strip():
            raise ValueError("El turno debe ser una cadena no vacía.")
        if not isinstance(horas, int) or horas <= 0:
            raise ValueError("Las horas deben ser un entero positivo.")
        if not isinstance(salario, (int, float)) or salario < 0:
            raise ValueError("El salario debe ser un número no negativo.")
        if not isinstance(password, str) or not password.strip():
            raise ValueError("La contraseña debe ser una cadena no vacía.")

        super().__init__(id, nombre, apellido, edad, genero,rol='trabajador', password=password)
        self.turno = turno
        self.horas = horas
        self._salario = salario

    def cambiar_turno(self, nuevo_turno: str) -> None:
        """
        Cambia el turno actual del trabajador.

        Parámetros
        ----------
        nuevo_turno : str
            Nuevo turno que se asignará al trabajador.
        """
        if not isinstance(nuevo_turno, str) or not nuevo_turno.strip(): #Si el nuevo turno que se inserta no es cadena de texto o está vacío salta error
            raise ValueError("El nuevo turno debe ser una cadena no vacía.")
        else:
            self.turno = nuevo_turno #Cambia el turno anterior por el nuevo insertado
            print(f"El turno ha sido cambiado a {self.turno}.")

    def calcular_salario_anual(self) -> float:
        """
        Calcula el salario anual del trabajador.

        Devuelve
        -------
        float
            Salario anual del trabajador.
        """
        return self._salario * 12