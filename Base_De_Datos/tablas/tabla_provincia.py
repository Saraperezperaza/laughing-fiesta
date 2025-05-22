import sqlite3
import os
from typing import List, Tuple

# Base de datos en la misma carpeta que este script
_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdd.db')

def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite.

    Returns
    -------
    sqlite3.Connection
        Conexión activa al archivo de base de datos.
    """
    conn = sqlite3.connect(_db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def crear_tabla_provincias() -> None:
    """
    Crea la tabla 'provincias' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : int
        Identificador único autoincremental (clave primaria).
    - nombre_comunidad : str
        Nombre de la comunidad autónoma.
    - nombre_provincia : str
        Nombre de la provincia (único).
    - presupuesto : float
        Presupuesto asignado; por defecto 0.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS provincias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_comunidad TEXT NOT NULL,
            nombre_provincia TEXT NOT NULL UNIQUE,
            presupuesto REAL NOT NULL DEFAULT 0
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_provincia(
    nombre_comunidad: str,
    nombre_provincia: str,
    presupuesto: float = 0
) -> None:
    """
    Inserta una nueva provincia en la tabla 'provincias'.

    Parameters
    ----------
    nombre_comunidad : str
        Nombre de la comunidad autónoma.
    nombre_provincia : str
        Nombre de la provincia (debe ser único).
    presupuesto : float, optional
        Presupuesto inicial; por defecto 0.

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
            "INSERT INTO provincias (nombre_comunidad, nombre_provincia, presupuesto) VALUES (?, ?, ?);",
            (nombre_comunidad, nombre_provincia, presupuesto)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar provincia: {e}")
    finally:
        conn.close()


def leer_provincias() -> List[Tuple[int, str, str, float]]:
    """
    Recupera todas las provincias almacenadas.

    Returns
    -------
    List[Tuple[int, str, str, float]]
        Tuplas con campos:
        (id, nombre_comunidad, nombre_provincia, presupuesto).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre_comunidad, nombre_provincia, presupuesto FROM provincias;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_provincia(nombre_provincia: str) -> None:
    """
    Elimina una provincia de la base de datos por su nombre.

    Parameters
    ----------
    nombre_provincia : str
        Nombre de la provincia a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM provincias WHERE nombre_provincia = ?;",
        (nombre_provincia,)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_provincias()
