import bcrypt as bcrypt

class Persona:
    """
    Clase que representa a una persona, con atributos básicos como id, nombre, apellido, edad, genero,
    y rol. Además, incluye un atributo de password hashado para seguridad.

    Atributos:
    id (str): Identificador único de la persona.
    nombre (str): Nombre de la persona.
    apellido (str): Apellido de la persona.
    edad (int): Edad de la persona.
    genero (str): Género de la persona.
    password_hash (str): Contraseña hasheada de la persona.
    rol (str): Rol o puesto que ocupa la persona (por ejemplo, 'paciente', 'médico').

    Métodos:
    a_diccionario(): Devuelve un diccionario con los atributos básicos de la persona.
    verificar_password(password: str) -> bool: Verifica si la contraseña proporcionada coincide con el hash guardado.
    __str__(): Devuelve una cadena con la información básica de la persona.
    """

    def __init__(self, id: str, nombre: str, apellido: str, edad: int, genero: str, rol: str, password: str) -> None:
        """
        Inicializa una nueva instancia de la clase Persona.

        Parámetros:
        id (str): Identificador único de la persona.
        nombre (str): Nombre de la persona.
        apellido (str): Apellido de la persona.
        edad (int): Edad de la persona.
        genero (str): Género de la persona.
        rol (str): Rol o puesto que ocupa la persona (por ejemplo, 'paciente', 'médico').
        password (str): Contraseña de la persona. Se guardará como hash.
        """

        self.id = id
        self._nombre = nombre
        self._apellido = apellido
        self.edad = edad
        self._genero = genero
        self.__password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # Convierte la contraseña en bytes, genera un salt y la hashea con bcrypt para guardarla de forma segura
        self._rol = rol

    def a_diccionario(self) -> dict:
        """
        Convierte los atributos básicos de la persona en un diccionario.

        Devuelve:
        dict: Diccionario con los atributos básicos de la persona.
        """
        return {
            'id': self.id,
            'nombre': self._nombre,
            'apellido': self._apellido,
            'edad': self.edad,
            'genero': self._genero,
            'rol': self._rol,
            'password_hash': self.__password_hash,
        }

    def verificar_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con el hash guardado.

        Parámetros:
        password (str): La contraseña a verificar.

        Devuelve:
        bool: True si la contraseña coincide con el hash, False de lo contrario.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.__password_hash) #compara la nueva contraseña escrita con el hash guardado

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de la persona.

        Devuelve:
        str: Una cadena con la información básica de la persona.
        """

        return(f'ID: {self.id} - Nombre: {self._nombre} - Apellido {self._apellido} - Edad {self.edad} - Género {self._genero}')