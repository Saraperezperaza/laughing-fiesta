class Ambulancia:
    """
    Clase que representa una ambulancia dentro del sistema hospitalario.

    Atributos
    ----------
    matricula : str
        Matrícula identificativa de la ambulancia.
    zona : str
        Zona geográfica asignada a la ambulancia.
    modelo : str
        Modelo del vehículo.
    sirena : str
        Tipo de sirena instalada en la ambulancia (bitonal o secuencial).
    paramedicos : list
        Lista de paramédicos asignados a la ambulancia.

    Clase Atributos
    ---------------
    cantidad : int
        Número total de ambulancias instanciadas.

    Métodos
    -------
    cantidad_ambulancias():
        Retorna la cantidad de ambulancias creadas.
    agregar_paramedico(paramedico):
        Asigna un paramédico a la ambulancia si no está ya asignado.
    recoger_paciente(paciente):
        Asigna un paciente a la ambulancia y retorna la velocidad estimada
        según la gravedad del estado del paciente.
    __str__():
        Retorna una representación legible de la ambulancia.
    """

    cantidad: int = 0

    def __init__(self, matricula: str, zona: str, modelo: str, sirena: str) -> None:
        """
        Inicializa una instancia de Ambulancia.

        Parámetros
        ----------
        matricula : str
            Matrícula de la ambulancia.
        zona : str
            Zona de cobertura de la ambulancia.
        modelo : str
            Modelo del vehículo.
        sirena : str
            Tipo de sirena ('bitonal' o 'secuencial').

        Excepciones
        ------
        ValueError
            Si la sirena no es 'bitonal' ni 'secuencial'.
        """
        self.__matricula = matricula
        self._zona = zona
        self.modelo = modelo
        try:
            if sirena not in ['bitonal', 'secuencial']: #Manejo de errores, la sirena solo puede ser bitonal o secuencial
                raise ValueError # Si no es bitonal o secuencial salta ValueError
            else:
                self.sirena = sirena
        except ValueError: #Definir el mensaje que sale cuando introducimos una sirena no válida
            print('Ese tono de sirena no existe en esa base de datos. Prueba con "bitonal" o "secuencial". Se cambiará el tono por defecto a bitonal')
            self.sirena = 'bitonal' # ponemos la bitonal por defecto
        self._paramedicos: list = []
        self._paciente = None
        Ambulancia.cantidad += 1

    @classmethod
    def cantidad_ambulancias(cls) -> int:
        """
        Devuelve la cantidad total de ambulancias creadas.

        Devuelve
        -------
        int
            Número total de ambulancias.
        """
        return cls.cantidad # devolvemos la cantidad de ambulancias creadas

    def agregar_paramedico(self, paramedico) -> None:
        """
        Asigna un paramédico a la ambulancia si no está ya asignado.

        Parámetros
        ----------
        paramedico : object
            Instancia de un paramédico.
        """
        if paramedico in self._paramedicos:
            print(f'El paramédico {paramedico.nombre} ya está en esta ambulancia.')
            return
        else:
            self._paramedicos.append(paramedico) # SI el paramedico no esta en la lista de paramedicos, lo añadimos

    def recoger_paciente(self, paciente) -> int:
        """
        Asigna un paciente a la ambulancia y determina la velocidad
        máxima estimada según el estado del paciente.

        Parámetros
        ----------
        paciente : object
            Instancia de un paciente con atributo `estado`.

        Devuelve
        -------
        int
            Velocidad máxima permitida en km/h basada en la urgencia del paciente.
        """
        self._paciente = paciente
        estado = self._paciente.estado.lower()
        if estado == 'urgente':
            return 200 # 200 es la velocidad maxima si el paciente está en estado urgente
        elif estado == 'grave':
            return 150
        elif estado == 'leve':
            return 90
        else:
            return 0

    def __str__(self) -> str:
        """
        Representación en cadena de la ambulancia.

        Devuelve
        -------
        str
            Información legible de la ambulancia.
        """
        if self._paramedicos:
            paramedico_info=[] # si hay algo en la lista paramedicos, creamos otra lista vacia llamada paramedico_info
            for paramedico in self._paramedicos: # Recorremos los paramedicos en la lista y los vamos añadiendo
                paramedico_info.append(paramedico.nombre)
        else:
            paramedico_info = 'Ninguno'
        return f'Ambulancia {self.__matricula} - Zona: {self._zona} - Modelo: {self.modelo} - Sirena: {self.sirena} - Paramedicos {paramedico_info}'
