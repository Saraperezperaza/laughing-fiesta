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


def crear_tabla_enfermeros() -> None:
    """
    Crea la tabla 'enfermeros' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único del enfermero (clave primaria).
    - especialidad : TEXT
        Especialidad médica del enfermero.
    - antiguedad : INTEGER
        Años de experiencia laboral.
    - username : TEXT
        Nombre de usuario único.
    - password : TEXT
        Contraseña del enfermero.
    - rol : TEXT
        Rol asignado; por defecto 'enfermero'.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS enfermeros (
            id TEXT PRIMARY KEY,
            especialidad TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'enfermero'
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_enfermero(
    enfermero_id: str,
    especialidad: str,
    antiguedad: int,
    username: str,
    password: str,
    rol: str = 'enfermero'
) -> None:
    """
    Inserta un nuevo enfermero en la tabla 'enfermeros'.

    Parameters
    ----------
    enfermero_id : str
        Identificador único del enfermero.
    especialidad : str
        Especialidad del enfermero.
    antiguedad : int
        Años de experiencia.
    username : str
        Nombre de usuario único.
    password : str
        Contraseña.
    rol : str, optional
        Rol asignado; por defecto 'enfermero'.

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
            "INSERT INTO enfermeros (id, especialidad, antiguedad, username, password, rol) VALUES (?, ?, ?, ?, ?, ?);",
            (enfermero_id, especialidad, antiguedad, username, password, rol)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar enfermero: {e}")
    finally:
        conn.close()


def leer_enfermeros() -> List[Tuple[str, str, int, str, str, str]]:
    """
    Recupera todos los enfermeros registrados.

    Returns
    -------
    List[Tuple[str, str, int, str, str, str]]
        Tuplas con campos:
        (id, especialidad, antiguedad, username, password, rol).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, especialidad, antiguedad, username, password, rol FROM enfermeros;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_enfermero(
    enfermero_id: str,
    especialidad: Optional[str] = None,
    antiguedad: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    rol: Optional[str] = None
) -> None:
    """
    Actualiza los datos de un enfermero existente.

    Parameters
    ----------
    enfermero_id : str
        Identificador del enfermero a actualizar.
    especialidad : str, optional
        Nueva especialidad.
    antiguedad : int, optional
        Nuevos años de experiencia.
    username : str, optional
        Nuevo nombre de usuario.
    password : str, optional
        Nueva contraseña.
    rol : str, optional
        Nuevo rol.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    if especialidad is not None:
        cursor.execute(
            "UPDATE enfermeros SET especialidad = ? WHERE id = ?;",
            (especialidad, enfermero_id)
        )
    if antiguedad is not None:
        cursor.execute(
            "UPDATE enfermeros SET antiguedad = ? WHERE id = ?;",
            (antiguedad, enfermero_id)
        )
    if username is not None:
        cursor.execute(
            "UPDATE enfermeros SET username = ? WHERE id = ?;",
            (username, enfermero_id)
        )
    if password is not None:
        cursor.execute(
            "UPDATE enfermeros SET password = ? WHERE id = ?;",
            (password, enfermero_id)
        )
    if rol is not None:
        cursor.execute(
            "UPDATE enfermeros SET rol = ? WHERE id = ?;",
            (rol, enfermero_id)
        )
    conn.commit()
    conn.close()


def eliminar_enfermero(enfermero_id: str) -> None:
    """
    Elimina un enfermero de la base de datos por su identificador.

    Parameters
    ----------
    enfermero_id : str
        Identificador único del enfermero a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enfermeros WHERE id = ?;', (enfermero_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_enfermeros()


