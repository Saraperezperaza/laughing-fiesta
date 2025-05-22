from Clases_Base_de_datos.provincia import Provincia
class Centro(Provincia):
    """
    Clase que representa un centro médico. Hereda de la clase `Provincia` y gestiona información
    sobre el centro, como su ID, nombre, presupuesto, trabajadores, y habitaciones disponibles.

    Atributos
    ---------
    ids_usados : set
        Conjunto que almacena los IDs de los centros ya usados para evitar duplicados.
    id_centro : str
        Identificador único del centro médico.
    nombre_centro : str
        Nombre del centro médico.
    cantidad_trabajadores : int
        Número de trabajadores en el centro médico.
    presupuesto : float
        Presupuesto del centro médico.
    habitaciones : int
        Número de habitaciones disponibles en el centro médico.

    Métodos
    --------
    __init__(self, nombre_comunidad, nombre_provincia, id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones)
        Inicializa una instancia de la clase `Centro`, validando que el ID sea único y los valores sean válidos.

    añadir_trabajadores(self, nueva_cantidad)
        Añade una cantidad de trabajadores al centro, validando que la cantidad sea positiva.

    añadir_habitaciones(self, cantidad_habitaciones)
        Añade una cantidad de habitaciones al centro, validando que la cantidad sea positiva.

    pagos(self, pago)
        Realiza un pago al presupuesto del centro, validando que no se haga un pago que deje el presupuesto negativo.

    obtener_info(self)
        Devuelve una cadena con la información básica del centro médico, incluyendo su ID, nombre, cantidad de trabajadores,
        habitaciones disponibles y presupuesto.

    Excepciones
    ---------
    ValueError
        Si el ID ya ha sido utilizado, si se intenta asignar un presupuesto, trabajadores o habitaciones negativos,
        o si los valores proporcionados no son válidos.
    """

    ids_usados = set()  # Conjunto que almacena los IDs ya usados de los centros.

    def __init__(self, nombre_comunidad: str, nombre_provincia: str, id_centro: str, nombre_centro: str,
                 cantidad_trabajadores: int, presupuesto: float, habitaciones: int):
        """
        Inicializa una instancia de `Centro` y valida que el ID sea único, que los valores sean válidos y ajusta los atributos.

        Parámetros
        ----------
        nombre_comunidad : str
            Nombre de la comunidad autónoma del centro.
        nombre_provincia : str
            Nombre de la provincia del centro.
        id_centro : str
            Identificador único del centro médico.
        nombre_centro : str
            Nombre del centro médico.
        cantidad_trabajadores : int
            Número de trabajadores del centro médico.
        presupuesto : float
            Presupuesto disponible para el centro médico.
        habitaciones : int
            Número de habitaciones disponibles en el centro.

        Excepciones
        ------
        ValueError
            Si el ID ya está en uso, si el presupuesto, la cantidad de trabajadores o habitaciones son negativos.
        """
        super().__init__(nombre_comunidad, nombre_provincia)
        self.id_centro = id_centro
        self.nombre_centro = nombre_centro
        self.cantidad_trabajadores = cantidad_trabajadores
        self.presupuesto = presupuesto
        self.habitaciones = habitaciones

        # Validación del ID
        if id_centro in Centro.ids_usados:
            raise ValueError(f'El ID: {id_centro} ya está en uso.')
        Centro.ids_usados.add(id_centro)

        # Validaciones para presupuesto, trabajadores y habitaciones
        if presupuesto < 0:
            raise ValueError('No se admiten presupuestos negativos')
        if cantidad_trabajadores < 0:
            raise ValueError('No se admiten cantidades negativas de trabajadores')
        if habitaciones < 0:
            raise ValueError('No se admiten habitaciones negativas')

    def anadir_trabajadores(self, nueva_cantidad: int) -> None:
        """
        Añade una cantidad de trabajadores al centro. La cantidad debe ser positiva.

        Parámetros
        ----------
        nueva_cantidad : int
            Número de trabajadores que se agregarán al centro.

        Excepciones
        ------
        ValueError
            Si la nueva cantidad es negativa.
        """
        if nueva_cantidad < 0:
            raise ValueError('No se admiten cantidades negativas de trabajadores')
        self.cantidad_trabajadores += nueva_cantidad

    def anadir_habitaciones(self, cantidad_habitaciones: int) -> None:
        """
        Añade una cantidad de habitaciones al centro. La cantidad debe ser positiva.

        Parámetros
        ----------
        cantidad_habitaciones : int
            Número de habitaciones que se agregarán al centro.

        Excepciones
        ------
        ValueError
            Si la cantidad de habitaciones es negativa.
        """
        if cantidad_habitaciones < 0:
            raise ValueError('No admiten cantidades negativas de habitaciones')
        self.habitaciones += cantidad_habitaciones

    def pagos(self, pago: float) -> None:
        """
        Realiza un pago que ajusta el presupuesto del centro. La operación no puede dejar el presupuesto en negativo.

        Parámetros
        ----------
        pago : float
            Cantidad a añadir al presupuesto (puede ser negativa).

        Excepciones
        ------
        ValueError
            Si el pago deja el presupuesto en negativo.
        """
        if self.presupuesto + pago < 0:
            raise ValueError('No se admiten presupuestos negativos')
        self.presupuesto += pago

    def obtener_info(self) -> str:
        """
        Devuelve una cadena con la información del centro, incluyendo su ID, nombre, cantidad de trabajadores, habitaciones
        disponibles y presupuesto.

        Devuelve
        -------
        str
            Información del centro.
        """
        info = f'Centro médico: {self.nombre_centro}\n'
        info += f'ID Centro: {self.id_centro}\n'
        info += f'Cantidad de trabajadores: {self.cantidad_trabajadores}\n'
        info += f'Habitaciones disponibles: {self.habitaciones}\n'
        info += f'Presupuesto: {self.presupuesto}€\n'
        return info