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


def crear_tabla_habitaciones() -> None:
    """
    Crea la tabla 'habitaciones' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - numero_habitacion : INTEGER
        Identificador único de la habitación (clave primaria).
    - capacidad : INTEGER
        Número máximo de pacientes permitidos.
    - limpia : INTEGER
        Indicador de limpieza (0: no, 1: sí), por defecto 0.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS habitaciones (
            numero_habitacion INTEGER PRIMARY KEY,
            capacidad INTEGER NOT NULL,
            limpia INTEGER NOT NULL DEFAULT 0
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_habitacion(
    numero_habitacion: int,
    capacidad: int,
    limpia: bool = False
) -> None:
    """
    Inserta una nueva habitación en la tabla 'habitaciones'.

    Parameters
    ----------
    numero_habitacion : int
        Identificador único de la habitación.
    capacidad : int
        Número máximo de pacientes permitidos.
    limpia : bool, optional
        Estado de limpieza (False: no limpia, True: limpia); por defecto False.

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
            "INSERT INTO habitaciones (numero_habitacion, capacidad, limpia) VALUES (?, ?, ?);",
            (numero_habitacion, capacidad, int(limpia))
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar habitación: {e}")
    finally:
        conn.close()


def leer_habitaciones() -> List[Tuple[int, int, int]]:
    """
    Recupera todas las habitaciones almacenadas.

    Returns
    -------
    List[Tuple[int, int, int]]
        Tuplas con campos:
        (numero_habitacion, capacidad, limpia).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT numero_habitacion, capacidad, limpia FROM habitaciones;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def limpiar_habitacion(numero_habitacion: int) -> None:
    """
    Marca una habitación como limpia (limpia = 1).

    Parameters
    ----------
    numero_habitacion : int
        Identificador de la habitación a actualizar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE habitaciones SET limpia = 1 WHERE numero_habitacion = ?;",
        (numero_habitacion,)
    )
    conn.commit()
    conn.close()


def eliminar_habitacion(numero_habitacion: int) -> None:
    """
    Elimina una habitación de la base de datos por su identificador.

    Parameters
    ----------
    numero_habitacion : int
        Identificador de la habitación a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM habitaciones WHERE numero_habitacion = ?;', (numero_habitacion,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_habitaciones()
