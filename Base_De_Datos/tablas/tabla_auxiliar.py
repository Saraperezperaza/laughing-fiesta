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


def crear_tabla_auxiliares() -> None:
    """
    Crea la tabla 'auxiliares' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT PRIMARY KEY
    - antiguedad : INTEGER NOT NULL
    - id_enfermero : TEXT UNIQUE
    - rol : TEXT NOT NULL DEFAULT 'auxiliar'

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS auxiliares (
            id TEXT PRIMARY KEY,
            antiguedad INTEGER NOT NULL,
            id_enfermero TEXT UNIQUE,
            rol TEXT NOT NULL DEFAULT 'auxiliar',
            FOREIGN KEY (id_enfermero) REFERENCES enfermeros(id) ON DELETE seT NULL
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_auxiliar(
    id: str,
    antiguedad: int,
    id_enfermero: Optional[str] = None,
    rol: str = 'auxiliar'
) -> None:
    """
    Inserta un nuevo auxiliar en la tabla 'auxiliares'.

    Parameters
    ----------
    id : str
        Identificador único del auxiliar.
    antiguedad : int
        Años de antigüedad del auxiliar.
    id_enfermero : Optional[str]
        Identificador del enfermero asociado (uno a uno).
    rol : str
        Rol del auxiliar; por defecto 'auxiliar'.

    Raises
    ------
    ValueError
        Si falla la integridad de la inserción.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO auxiliares (id, antiguedad, id_enfermero, rol) VALUES (?, ?, ?, ?);",
            (id, antiguedad, id_enfermero, rol)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar auxiliar: {e}")
    finally:
        conn.close()


def leer_auxiliares() -> List[Tuple[str, int, Optional[str], str]]:
    """
    Recupera todos los auxiliares registrados.

    Returns
    -------
    List[Tuple[str, int, Optional[str], str]]
        Tuplas con campos:
        (id, antiguedad, id_enfermero, rol).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, antiguedad, id_enfermero, rol FROM auxiliares;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_auxiliar(
    id: str,
    antiguedad: Optional[int] = None,
    id_enfermero: Optional[str] = None,
    rol: Optional[str] = None
) -> None:
    """
    Actualiza los datos de un auxiliar existente.

    Parameters
    ----------
    id : str
        Identificador del auxiliar a actualizar.
    antiguedad : Optional[int]
        Nueva antigüedad.
    id_enfermero : Optional[str]
        Nuevo identificador del enfermero asociado.
    rol : Optional[str]
        Nuevo rol.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    if antiguedad is not None:
        cursor.execute(
            "UPDATE auxiliares SET antiguedad = ? WHERE id = ?;",
            (antiguedad, id)
        )
    if id_enfermero is not None:
        cursor.execute(
            "UPDATE auxiliares SET id_enfermero = ? WHERE id = ?;",
            (id_enfermero, id)
        )
    if rol is not None:
        cursor.execute(
            "UPDATE auxiliares SET rol = ? WHERE id = ?;",
            (rol, id)
        )
    conn.commit()
    conn.close()


def eliminar_auxiliar(id: str) -> None:
    """
    Elimina un auxiliar de la base de datos por su id.

    Parameters
    ----------
    id : str
        Identificador del auxiliar a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM auxiliares WHERE id = ?;', (id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_auxiliares()