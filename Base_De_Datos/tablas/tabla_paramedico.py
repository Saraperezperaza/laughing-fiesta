import sqlite3
import os
from typing import List, Tuple, Optional

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


def crear_tabla_paramedicos() -> None:
    """
    Crea la tabla 'paramedicos' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único del paramédico (clave primaria).
    - especialidad : TEXT
        Especialidad médica del paramédico.
    - antiguedad : INTEGER
        Años de experiencia laboral.
    - id_ambulancia : TEXT, opcional
        Matrícula de la ambulancia asignada.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS paramedicos (
            id TEXT PRIMARY KEY,
            especialidad TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            id_ambulancia TEXT
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_paramedico(
    paramedico_id: str,
    especialidad: str,
    antiguedad: int,
    id_ambulancia: Optional[str] = None
) -> None:
    """
    Inserta un nuevo paramédico en la tabla 'paramedicos'.

    Parameters
    ----------
    paramedico_id : str
        Identificador único del paramédico.
    especialidad : str
        Especialidad médica del paramédico.
    antiguedad : int
        Años de experiencia.
    id_ambulancia : str, optional
        Matrícula de la ambulancia asignada; por defecto None.

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
            "INSERT INTO paramedicos (id, especialidad, antiguedad, id_ambulancia) VALUES (?, ?, ?, ?);",
            (paramedico_id, especialidad, antiguedad, id_ambulancia)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar paramédico: {e}")
    finally:
        conn.close()


def leer_paramedicos() -> List[Tuple[str, str, int, Optional[str]]]:
    """
    Recupera todos los paramédicos almacenados.

    Returns
    -------
    List[Tuple[str, str, int, Optional[str]]]
        Tuplas con campos:
        (id, especialidad, antiguedad, id_ambulancia).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, especialidad, antiguedad, id_ambulancia FROM paramedicos;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_paramedico(paramedico_id: str) -> None:
    """
    Elimina un paramédico de la base de datos por su identificador.

    Parameters
    ----------
    paramedico_id : str
        Identificador del paramédico a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM paramedicos WHERE id = ?;",
        (paramedico_id,)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_paramedicos()
