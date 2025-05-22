import sqlite3
import os
from typing import List, Tuple

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


def crear_tabla_enfermedades() -> None:
    """
    Crea la tabla 'enfermedades' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único de la enfermedad (clave primaria).
    - nombre : TEXT
        Nombre de la enfermedad.
    - sintomas : TEXT
        Descripción de los síntomas.
    - cronica : INTEGER
        Indicador de cronicidad (0: no, 1: sí), por defecto 0.
    - grave : INTEGER
        Indicador de gravedad (0: no, 1: sí), por defecto 0.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS enfermedades (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            sintomas TEXT NOT NULL,
            cronica INTEGER NOT NULL DEFAULT 0,
            grave INTEGER NOT NULL DEFAULT 0
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_enfermedad(
    enfermedad_id: str,
    nombre: str,
    sintomas: str,
    cronica: bool = False,
    grave: bool = False
) -> None:
    """
    Inserta una nueva enfermedad en la tabla 'enfermedades'.

    Parameters
    ----------
    enfermedad_id : str
        Identificador único de la enfermedad.
    nombre : str
        Nombre de la enfermedad.
    sintomas : str
        Descripción de los síntomas asociados.
    cronica : bool, optional
        Indica si la enfermedad es crónica; por defecto False.
    grave : bool, optional
        Indica si la enfermedad es grave; por defecto False.

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
            "INSERT INTO enfermedades (id, nombre, sintomas, cronica, grave) VALUES (?, ?, ?, ?, ?);",
            (enfermedad_id, nombre, sintomas, int(cronica), int(grave))
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar enfermedad: {e}")
    finally:
        conn.close()


def leer_enfermedades() -> List[Tuple[str, str, str, int, int]]:
    """
    Recupera todas las enfermedades almacenadas en la base de datos.

    Returns
    -------
    List[Tuple[str, str, str, int, int]]
        Tuplas con campos:
        (id, nombre, sintomas, cronica, grave).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, sintomas, cronica, grave FROM enfermedades;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def marcar_enfermedad_grave(enfermedad_id: str) -> None:
    """
    Marca una enfermedad como grave (grave = 1).

    Parameters
    ----------
    enfermedad_id : str
        Identificador de la enfermedad a actualizar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE enfermedades SET grave = 1 WHERE id = ?;",
        (enfermedad_id,)
    )
    conn.commit()
    conn.close()


def eliminar_enfermedad(enfermedad_id: str) -> None:
    """
    Elimina una enfermedad de la base de datos por su identificador.

    Parameters
    ----------
    enfermedad_id : str
        Identificador único de la enfermedad a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enfermedades WHERE id = ?;', (enfermedad_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_enfermedades()

