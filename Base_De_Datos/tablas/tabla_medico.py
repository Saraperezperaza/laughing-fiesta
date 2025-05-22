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


def crear_tabla_medicos() -> None:
    """
    Crea la tabla 'medicos' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único del médico (clave primaria).
    - username : TEXT
        Nombre de usuario único para el médico.
    - password : TEXT
        Contraseña del médico.
    - especialidad : TEXT
        Especialidad médica.
    - antiguedad : INTEGER
        Años de experiencia.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS medicos (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            antiguedad INTEGER NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_medico(
    medico_id: str,
    username: str,
    password: str,
    especialidad: str,
    antiguedad: int
) -> None:
    """
    Inserta un nuevo médico en la tabla 'medicos'.

    Parameters
    ----------
    medico_id : str
        Identificador único del médico.
    username : str
        Nombre de usuario único.
    password : str
        Contraseña.
    especialidad : str
        Especialidad médica.
    antiguedad : int
        Años de experiencia.

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
            "INSERT INTO medicos (id, username, password, especialidad, antiguedad) VALUES (?, ?, ?, ?, ?);",
            (medico_id, username, password, especialidad, antiguedad)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar médico: {e}")
    finally:
        conn.close()


def leer_medicos() -> List[Tuple[str, str, str, str, int]]:
    """
    Recupera todos los médicos almacenados.

    Returns
    -------
    List[Tuple[str, str, str, str, int]]
        Tuplas con campos:
        (id, username, password, especialidad, antiguedad).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password, especialidad, antiguedad FROM medicos;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_medico(
    medico_id: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    especialidad: Optional[str] = None,
    antiguedad: Optional[int] = None
) -> None:
    """
    Actualiza los datos de un médico existente.

    Parameters
    ----------
    medico_id : str
        Identificador del médico a actualizar.
    username : str, optional
        Nuevo nombre de usuario.
    password : str, optional
        Nueva contraseña.
    especialidad : str, optional
        Nueva especialidad.
    antiguedad : int, optional
        Nuevos años de experiencia.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    if username is not None:
        cursor.execute(
            "UPDATE medicos SET username = ? WHERE id = ?;",
            (username, medico_id)
        )
    if password is not None:
        cursor.execute(
            "UPDATE medicos SET password = ? WHERE id = ?;",
            (password, medico_id)
        )
    if especialidad is not None:
        cursor.execute(
            "UPDATE medicos SET especialidad = ? WHERE id = ?;",
            (especialidad, medico_id)
        )
    if antiguedad is not None:
        cursor.execute(
            "UPDATE medicos SET antiguedad = ? WHERE id = ?;",
            (antiguedad, medico_id)
        )
    conn.commit()
    conn.close()


def eliminar_medico(medico_id: str) -> None:
    """
    Elimina un médico de la base de datos por su identificador.

    Parameters
    ----------
    medico_id : str
        Identificador del médico a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM medicos WHERE id = ?;",
        (medico_id,)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_medicos()


