import sqlite3
import os
from typing import List, Tuple, Optional

# Base de datos en la misma carpeta que este script
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdd.db')

def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite.

    Returns
    -------
    sqlite3.Connection
        Conexión activa al archivo de base de datos.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def crear_tabla_centros() -> None:
    """
    Crea la tabla 'centros' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id_centro : str
        Identificador único del centro, clave primaria.
    - nombre_centro : str
        Nombre del centro médico.
    - cantidad_trabajadores : int
        Número de trabajadores en el centro.
    - presupuesto : float
        Presupuesto asignado al centro.
    - habitaciones : int
        Número de habitaciones disponibles.
    - id_provincia : int
        Identificador de la provincia asociada.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS centros (
            id_centro TEXT PRIMARY KEY,
            nombre_centro TEXT NOT NULL,
            cantidad_trabajadores INTEGER NOT NULL,
            presupuesto REAL NOT NULL,
            habitaciones INTEGER NOT NULL,
            id_provincia INTEGER NOT NULL,
            FOREIGN KEY(id_provincia) REFERENCES provincias(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    conn.close()


def insertar_centro(
    id_centro: str,
    nombre_centro: str,
    cantidad_trabajadores: int,
    presupuesto: float,
    habitaciones: int,
    id_provincia: int
) -> None:
    """
    Inserta un nuevo centro en la tabla 'centros'.

    Parameters
    ----------
    id_centro : str
        Identificador único del centro.
    nombre_centro : str
        Nombre del centro médico.
    cantidad_trabajadores : int
        Número de trabajadores en el centro.
    presupuesto : float
        Presupuesto asignado al centro.
    habitaciones : int
        Número de habitaciones disponibles.
    id_provincia : int
        Identificador de la provincia asociada.

    Raises
    ------
    ValueError
        Si la inserción viola restricciones de integridad.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO centros (id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones, id_provincia) VALUES (?, ?, ?, ?, ?, ?);",
            (id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones, id_provincia)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar centro: {e}")
    finally:
        conn.close()


def leer_centros() -> List[Tuple[str, str, int, float, int, int]]:
    """
    Recupera todos los registros de la tabla 'centros'.

    Returns
    -------
    List[Tuple[str, str, int, float, int, int]]
        Tuplas con campos:
        (id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones, id_provincia).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones, id_provincia FROM centros;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_centro(
    id_centro: str,
    nombre_centro: Optional[str] = None,
    cantidad_trabajadores: Optional[int] = None,
    presupuesto: Optional[float] = None,
    habitaciones: Optional[int] = None,
    id_provincia: Optional[int] = None
) -> None:
    """
    Actualiza los datos de un centro existente.

    Parameters
    ----------
    id_centro : str
        Identificador del centro a actualizar.
    nombre_centro : Optional[str]
        Nuevo nombre del centro.
    cantidad_trabajadores : Optional[int]
        Nueva cantidad de trabajadores.
    presupuesto : Optional[float]
        Nuevo presupuesto asignado.
    habitaciones : Optional[int]
        Nuevo número de habitaciones.
    id_provincia : Optional[int]
        Nuevo identificador de provincia.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    if nombre_centro is not None:
        cursor.execute(
            "UPDATE centros SET nombre_centro = ? WHERE id_centro = ?;",
            (nombre_centro, id_centro)
        )
    if cantidad_trabajadores is not None:
        cursor.execute(
            "UPDATE centros SET cantidad_trabajadores = ? WHERE id_centro = ?;",
            (cantidad_trabajadores, id_centro)
        )
    if presupuesto is not None:
        cursor.execute(
            "UPDATE centros SET presupuesto = ? WHERE id_centro = ?;",
            (presupuesto, id_centro)
        )
    if habitaciones is not None:
        cursor.execute(
            "UPDATE centros SET habitaciones = ? WHERE id_centro = ?;",
            (habitaciones, id_centro)
        )
    if id_provincia is not None:
        cursor.execute(
            "UPDATE centros SET id_provincia = ? WHERE id_centro = ?;",
            (id_provincia, id_centro)
        )
    conn.commit()
    conn.close()


def eliminar_centro(id_centro: str) -> None:
    """
    Elimina un centro de la base de datos por su identificador.

    Parameters
    ----------
    id_centro : str
        Identificador del centro a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM centros WHERE id_centro = ?;', (id_centro,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_centros()
