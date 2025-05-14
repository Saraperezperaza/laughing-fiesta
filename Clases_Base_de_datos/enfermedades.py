class Enfermedad:
    """
    Clase que representa una enfermedad, con atributos como el nombre, los síntomas, la condición de crónica,
    su gravedad y la lista de pacientes afectados por la enfermedad.

    Atributos
    ----------
    nombre : str
        Nombre de la enfermedad.
    sintomas : str
        Síntomas asociados a la enfermedad.
    cronica : bool
        Indica si la enfermedad es crónica. Por defecto es False.
    grave : bool
        Indica si la enfermedad ha sido marcada como grave. Por defecto es False.
    pacientes : list
        Lista de pacientes que están afectados por esta enfermedad.

    Métodos
    -------
    marcar_grave() :
        Marca la enfermedad como grave, cambiando el estado del atributo `grave` a True.
        Devuelve un mensaje indicando que la enfermedad ha sido marcada como grave.

    obtener_info() :
        Devuelve un resumen con la información de la enfermedad: nombre, síntomas, si es crónica y si es grave.

    paciente_tiene_enfermedad(paciente) :
        Asigna la enfermedad al paciente si no la tiene ya asignada. Si el paciente ya está asignado, muestra un mensaje.
        También asigna la enfermedad al paciente a través del método asignar_enfermedad de la clase Paciente.

    listado_pacientes() :
        Devuelve la lista de pacientes afectados por la enfermedad.
    """

    def __init__(self, nombre: str, sintomas: str, cronica: bool = False):
        """
        Inicializa una instancia de `Enfermedad` con nombre, síntomas y la condición de si es crónica o no.

        Parámetros
        ----------
        nombre : str
            Nombre de la enfermedad.
        sintomas : str
            Síntomas asociados a la enfermedad.
        cronica : bool, opcional
            Indica si la enfermedad es crónica. Por defecto es False.

        Excepciones
        ------------
        ValueError
            Si no se proporciona nombre o síntomas.
        """
        if not nombre or not sintomas:
            raise ValueError('Debe proporcionar nombre y síntomas para la enfermedad.')
        self.nombre = nombre
        self.sintomas = sintomas
        self.cronica = cronica
        self.grave = False
        self.pacientes = []

    def marcar_grave(self) -> str:
        """
        Marca la enfermedad como grave, estableciendo el atributo `grave` a True.

        Devuelve
        -------
        str
            Mensaje indicando que la enfermedad ha sido marcada como grave.
        """
        self.grave = True
        return f'La enfermedad: {self.nombre} ha sido marcada como grave.'

    def obtener_info(self) -> str:
        """
        Devuelve un resumen de la información de la enfermedad.

        Devuelve
        -------
        str
            Información sobre el nombre, los síntomas, si es crónica y si es grave.
        """
        return (f'Enfermedad: {self.nombre}\n'
                f'Síntomas: {self.sintomas}\n'
                f'Crónica: {self.cronica}\n'
                f'Grave: {self.grave}\n')

    def paciente_tiene_enfermedad(self, paciente: object) -> None:
        """
        Asigna la enfermedad al paciente si no la tiene ya asignada.

        Si el paciente ya tiene la enfermedad, muestra un mensaje indicándolo.

        Parámetros
        ----------
        paciente : object
            El paciente al que se le asignará la enfermedad.

        Excepciones
        ------------
        None
        """
        if paciente not in self.pacientes:
            self.pacientes.append(paciente)
            paciente.asignar_enfermedades(self)
        else:
            print('El paciente ya tiene esa enfermedad asignada')

    def listado_pacientes(self) -> list:
        """
        Devuelve la lista de pacientes afectados por la enfermedad.

        Devuelve
        -------
        list
            Lista de pacientes afectados por la enfermedad.
        """
        listado = []
        for paciente in self.pacientes:
            listado.append(str(paciente))
        return listado

