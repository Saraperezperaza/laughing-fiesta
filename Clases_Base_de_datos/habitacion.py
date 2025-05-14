class Habitacion:
    """
    Clase que representa una habitación del hospital.

    Atributos
    ----------
    numero_habitacion : int
        Número identificador de la habitación.
    capacidad : int
        Número máximo de pacientes que pueden estar en la habitación.
    limpia : bool
        Indica si la habitación está limpia o no.
    pacientes : list
        Lista de pacientes actualmente asignados a la habitación.
    historial_pacientes : list
        Historial de todos los pacientes que han pasado por la habitación.
    pacientes_info : list
        Lista de nombres de los pacientes actuales (como cadenas).
    """

    def __init__(self, numero_habitacion: int, capacidad: int, limpia: bool = False) -> None:
        """
        Inicializa una instancia de Habitacion.

        Parámetros
        ----------
        numero_habitacion : int
            Número de habitación.
        capacidad : int
            Capacidad máxima de la habitación.
        limpia : bool, opcional
            Estado inicial de limpieza (por defecto es False).
        """
        self.numero_habitacion = numero_habitacion
        self.capacidad = capacidad
        self.limpia = limpia
        self._pacientes = []
        self._historial_pacientes = []
        self.pacientes_info = []

    def obtener_info(self) -> str:
        """
        Genera una cadena con información general de la habitación.

        Returns
        -------
        str
            Información detallada de la habitación: número, limpieza, capacidad, pacientes actuales y cantidad.
        """
        for paciente in self._pacientes: #Recorre la lista de pacientes y añade el nombre de cada paciente a la lista
            self.pacientes_info.append(str(paciente.nombre))
        info = f'Habitacion: {self.numero_habitacion} - Limpia: {self.limpia} - Capacidad: {self.capacidad} - Pacientes asignados: {self.pacientes_info} - Cantidad de pacientes: {len(self._pacientes)}'
        return info

    def __len__(self) -> int:
        """
        Devuelve la cantidad actual de pacientes asignados.

        Devuelve
        -------
        int
            Número de pacientes en la habitación.
        """
        return len(self._pacientes) #Para luego verificar si hay espacio en la habitación

    def limpiar(self) -> None:
        """
        Limpia la habitación si no lo está.
        """
        if not self.limpia:
            self.limpia = True
            print(f'La habitación {self.numero_habitacion} ha sido limpiada.')
        else:
            print(f'La habitación {self.numero_habitacion} ya está limpia.')

    def anadir_pacientes(self, paciente: object)-> list:
        """
        Añade un paciente a la habitación si hay espacio y no está repetido.

        Parámetros
        ----------
        paciente : object
            Objeto que representa a un paciente (se espera que tenga atributo 'nombre').

        Devuelve
        -------
        list
            Lista actualizada de pacientes en la habitación.

        Errores
        ------
        ValueError
            Si la habitación está llena o el paciente ya está asignado.
        """
        if len(self) >= self.capacidad: #Si se quieren añadir más pacientes de la capacidad de la habitación
            raise ValueError(
                f'La cantidad de pacientes de la habitación {self.numero_habitacion} sobrepasa su capacidad: {self.capacidad}'
            )
        if paciente in self._pacientes: #Si el paciente ya está en la habitación
            raise ValueError(
                f'El paciente ya está registrado en la habitación {self.numero_habitacion}'
            )
        else: #Si los pacientes caben y no están registrados previamente en una habitación
            self._pacientes.append(paciente)
            self._historial_pacientes.append(paciente)
        return self._pacientes

