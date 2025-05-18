from Clases_Base_de_datos.comunidad import Comunidad


class Provincia(Comunidad):
    """
    Clase que representa una provincia dentro de una comunidad autónoma. Hereda de la clase Comunidad y permite gestionar
    los centros médicos dentro de una provincia, proporcionando funcionalidades para añadir, eliminar y buscar centros médicos.

    Atributos
    ----------
    nombre_comunidad : str
        Nombre de la comunidad autónoma a la que pertenece la provincia.
    nombre_provincia : str
        Nombre de la provincia.
    centros : list
        Lista que almacena los centros médicos registrados en la provincia.

    Métodos
    -------
    __init__(nombre_comunidad: str, nombre_provincia: str) -> None
        Inicializa los atributos de la provincia, incluyendo el nombre de la comunidad, el nombre de la provincia y la lista de centros.

    obtener_info() -> str
        Devuelve una cadena con la información detallada de la comunidad, la provincia, la cantidad de centros médicos y el presupuesto.

    añadir_centro(centro) -> str
        Añade un centro médico a la provincia si no está ya registrado. Si el centro ya existe, se muestra un mensaje de advertencia.

    eliminar_centro(centro) -> str
        Elimina un centro médico de la provincia si está registrado. Si el centro no está registrado, se muestra un mensaje de advertencia.

    buscar_centro(nombre_centro) -> Union[Centro, str]
        Busca un centro médico por su nombre dentro de la provincia. Si el centro se encuentra, devuelve el objeto del centro,
        de lo contrario, muestra un mensaje indicando que no se ha encontrado.
    """

    def __init__(self, nombre_comunidad: str, nombre_provincia: str) -> None:
        """
        Inicializa los atributos de la provincia, incluyendo el nombre de la comunidad, el nombre de la provincia y la lista de centros médicos.

        Parámetros
        ----------
        nombre_comunidad : str
            Nombre de la comunidad autónoma a la que pertenece la provincia.
        nombre_provincia : str
            Nombre de la provincia.
        """
        super().__init__(nombre_comunidad)
        self.nombre_provincia = nombre_provincia
        self._centros = []

    def obtener_info(self) -> str:
        """
        Devuelve una cadena con la información detallada de la comunidad, la provincia,
        la cantidad de centros médicos registrados en la provincia y el presupuesto.

        Devuelve
        -------
        str
            Información detallada de la provincia y la comunidad.
        """
        info = f'Comunidad: {self.nombre_comunidad}\n'
        info += f'Provincia: {self.nombre_provincia}\n'
        info += f'Centros médicos: {len(self._centros)}\n'
        info += f'Presupuesto: {self.presupuesto}€\n'
        return info

    def anadir_centro(self, centro: object) -> str:
        """
        Añade un centro médico a la provincia si no está ya registrado. Si el centro ya existe,
        se devuelve un mensaje indicando que no se puede añadir.

        Parámetros
        ----------
        centro : Centro
            El objeto del centro médico a añadir a la provincia.

        Devuelve
        -------
        str
            Mensaje que indica si el centro fue añadido correctamente o no.
        """
        if centro in self._centros:
            return f'No puedes añadir este centro porque ya está registrado'
        else:
            self._centros.append(centro)
        return f'Se ha añadirdo el centro correctamente a la provincia {self.nombre_provincia}'

    def eliminar_centro(self, centro) -> str:
        """
        Elimina un centro médico de la provincia si está registrado. Si el centro no está registrado,
        se devuelve un mensaje indicando que no se puede eliminar.

        Parámetros
        ----------
        centro : Centro
            El objeto del centro médico a eliminar de la provincia.

        Devuelve
        -------
        str
            Mensaje que indica si el centro fue eliminado correctamente o no.
        """
        if centro not in self._centros:
            return f'No puedes eliminar el centro {centro.nombre_centro} porque este no está registrado'
        else:
            self._centros.remove(centro)
            return (
                f'Se ha eliminado el centro {centro.nombre_centro} correctamente a la provincia {self.nombre_provincia}')

    def buscar_centro(self, nombre_centro: str) -> str:
        """
        Busca un centro médico por su nombre dentro de la provincia. Si el centro se encuentra,
        devuelve el objeto del centro, de lo contrario, muestra un mensaje indicando que no se ha encontrado.

        Parámetros
        ----------
        nombre_centro : str
            Nombre del centro médico a buscar.

        Devuelve
        -------
        Union[Centro, str]
            El objeto del centro médico si se encuentra, o un mensaje indicando que no se ha encontrado.
        """
        for centro in self._centros:
            if centro.nombre_centro == nombre_centro:
                return centro
        return f'Centro {nombre_centro} no encontrado en la provincia {self.nombre_provincia}'
