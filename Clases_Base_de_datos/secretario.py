from trabajador import Trabajador
from documento import Documento

class Secretario(Trabajador, Documento):
    """
    Clase que representa a un secretario, quien es un trabajador que maneja documentos
    y realiza tareas administrativas dentro de un departamento.

    Hereda de:
        - Trabajador: para obtener atributos relacionados con el trabajo.
        - Documento: para manejar y firmar documentos.

    Atributos
    ----------
    id : str
        El identificador único del secretario.
    nombre : str
        El nombre del secretario.
    apellido : str
        El apellido del secretario.
    edad : int
        La edad del secretario.
    genero : str
        El género del secretario.
    turno : str
        El turno en el que trabaja el secretario.
    horas : int
        Las horas laborales que realiza el secretario.
    salario : float
        El salario del secretario.
    titulo : str
        El título académico del secretario.
    descripcion : str
        Una breve descripción del trabajo o responsabilidades del secretario.
    antiguedad : int
        Los años de experiencia del secretario en la empresa.
    email : str
        El correo electrónico del secretario.
    departamento : str
        El departamento al que pertenece el secretario.

    Métodos
    -------
    firma_documentos(documento : Documento) -> str
        Permite al secretario firmar un documento si es una instancia de la clase Documento.

    enviar_correo(destinatario : str, asunto : str, mensaje : str) -> str
        Envía un correo electrónico con el asunto y el mensaje proporcionados al destinatario.
    """

    def __init__(self, id: str, nombre: str, apellido: str, edad: int, genero: str, turno: str, horas: int,salario: float, titulo: str, descripcion: str, antiguedad: int, email: str, departamento: str):
        """
        Inicializa un nuevo objeto Secretario con la información proporcionada.

        Parámetros
        -----------
        id : str
            El identificador único del secretario.
        nombre : str
            El nombre del secretario.
        apellido : str
            El apellido del secretario.
        edad : int
            La edad del secretario.
        genero : str
            El género del secretario.
        turno : str
            El turno en el que trabaja el secretario.
        horas : int
            Las horas laborales que realiza el secretario.
        salario : float
            El salario del secretario.
        titulo : str
            El título académico del secretario.
        descripcion : str
            Una breve descripción del trabajo o responsabilidades del secretario.
        antiguedad : int
            Los años de experiencia del secretario en la empresa.
        email : str
            El correo electrónico del secretario.
        departamento : str
            El departamento al que pertenece el secretario.
        """
        Trabajador.__init__(self, id, nombre, apellido, edad, genero, turno, horas, salario)
        Documento.__init__(self, titulo, descripcion)
        self.antiguedad = antiguedad
        self.email = email
        self.departamento = departamento

    def enviar_correo(self, destinatario: str, asunto: str, mensaje: str) -> str:
        """
        Envía un correo electrónico con el asunto y mensaje proporcionados al destinatario.

        Parámetros
        -----------
        destinatario : str
            El destinatario del correo electrónico.
        asunto : str
            El asunto del correo electrónico.
        mensaje : str
            El cuerpo del mensaje del correo electrónico.

        Devuelve
        --------
        str
            Un mensaje confirmando que el correo ha sido enviado.
        """
        return f'Correo enviado a {destinatario} con asunto "{asunto}" y mensaje: {mensaje}'

