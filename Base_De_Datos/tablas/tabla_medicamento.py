import sqlite3
import os
from typing import List, Tuple, Optional, Union
from datetime import date, datetime

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


def crear_tabla_medicamentos() -> None:
    """
    Crea la tabla 'medicamentos' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único del medicamento (clave primaria).
    - nombre : TEXT
        Nombre del medicamento.
    - dosis : TEXT
        Dosis recomendada.
    - precio : float
        Precio del medicamento.
    - fecha_caducidad : TEXT
        Fecha de caducidad en formato 'YYYY-MM-DD'.
    - alergenos : TEXT
        Lista de alérgenos separados por comas (opcional).

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS medicamentos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            dosis TEXT NOT NULL,
            precio REAL NOT NULL,
            fecha_caducidad TEXT NOT NULL,
            alergenos TEXT
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_medicamento(
    medicamento_id: str,
    nombre: str,
    dosis: str,
    precio: float,
    fecha_caducidad: Union[date, datetime, str],
    alergenos: Optional[List[str]] = None
) -> None:
    """
    Inserta un nuevo medicamento en la tabla 'medicamentos'.

    Parameters
    ----------
    medicamento_id : str
        Identificador único del medicamento.
    nombre : str
        Nombre del medicamento.
    dosis : str
        Dosis recomendada.
    precio : float
        Precio del medicamento.
    fecha_caducidad : date | datetime | str
        Fecha de caducidad; si es date/datetime se formatea a 'YYYY-MM-DD'.
    alergenos : List[str], optional
        Lista de alérgenos; por defecto ninguna.

    Raises
    ------
    ValueError
        Si la inserción viola restricciones de integridad.

    Returns
    -------
    None
    """
    if isinstance(fecha_caducidad, (date, datetime)):
        fecha_caducidad = fecha_caducidad.strftime('%Y-%m-%d')
    alergenos_str = ','.join(alergenos) if alergenos else None
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO medicamentos (id, nombre, dosis, precio, fecha_caducidad, alergenos) VALUES (?, ?, ?, ?, ?, ?);",
            (medicamento_id, nombre, dosis, precio, fecha_caducidad, alergenos_str)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar medicamento: {e}")
    finally:
        conn.close()


def leer_medicamentos() -> List[Tuple[str, str, str, float, str, Optional[str]]]:
    """
    Recupera todos los medicamentos almacenados.

    Returns
    -------
    List[Tuple[str, str, str, float, str, Optional[str]]]
        Tuplas con campos:
        (id, nombre, dosis, precio, fecha_caducidad, alergenos).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, dosis, precio, fecha_caducidad, alergenos FROM medicamentos;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_medicamento(medicamento_id: str) -> None:
    """
    Elimina un medicamento de la base de datos por su identificador.

    Parameters
    ----------
    medicamento_id : str
        Identificador único del medicamento a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM medicamentos WHERE id = ?;",
        (medicamento_id,)
    )
    conn.commit()
    conn.close()


def crear_tabla_medicamento_enfermedad() -> None:
    """
    Crea la tabla 'medicamento_enfermedad' en la base de datos si no existe.

    Relaciona medicamentos con enfermedades (N:N).

    La tabla contiene:
    - medicamento_id : TEXT
    - enfermedad_id  : TEXT

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS medicamento_enfermedad (
            medicamento_id TEXT NOT NULL,
            enfermedad_id TEXT NOT NULL,
            PRIMARY KEY (medicamento_id, enfermedad_id),
            FOREIGN KEY(medicamento_id) REFERENCES medicamentos(id) ON DELETE CASCADE,
            FOREIGN KEY(enfermedad_id) REFERENCES enfermedades(id) ON DELETE CASCADE
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_medicamento_enfermedad(
    medicamento_id: str,
    enfermedad_id: str
) -> None:
    """
    Asocia un medicamento con una enfermedad.

    Parameters
    ----------
    medicamento_id : str
        Identificador del medicamento.
    enfermedad_id : str
        Identificador de la enfermedad.

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
            "INSERT INTO medicamento_enfermedad (medicamento_id, enfermedad_id) VALUES (?, ?);",
            (medicamento_id, enfermedad_id)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error al asociar medicamento y enfermedad: {e}")
    finally:
        conn.close()


def leer_medicamento_enfermedad() -> List[Tuple[str, str]]:
    """
    Recupera todas las asociaciones entre medicamentos y enfermedades.

    Returns
    -------
    List[Tuple[str, str]]
        Tuplas con campos:
        (medicamento_id, enfermedad_id).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT medicamento_id, enfermedad_id FROM medicamento_enfermedad;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_medicamento_enfermedad(
    medicamento_id: str,
    enfermedad_id: str
) -> None:
    """
    Elimina una asociación medicamento-enfermedad.

    Parameters
    ----------
    medicamento_id : str
        Identificador del medicamento.
    enfermedad_id : str
        Identificador de la enfermedad.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM medicamento_enfermedad WHERE medicamento_id = ? AND enfermedad_id = ?;",
        (medicamento_id, enfermedad_id)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_medicamentos()
    crear_tabla_medicamento_enfermedad()
