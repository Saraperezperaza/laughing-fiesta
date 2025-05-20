import sqlite3
import os
import json
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


def crear_tabla_pacientes() -> None:
    """
    Crea la tabla 'pacientes' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
      - id : TEXT
      - username : TEXT
      - password : TEXT
      - nombre : TEXT
      - apellido : TEXT
      - edad : INTEGER
      - genero : TEXT
      - estado : TEXT
      - historial_medico : TEXT (JSON)
      - id_enfermero : TEXT
      - id_medico : TEXT
      - id_habitacion : TEXT
      - rol : TEXT, por defecto 'paciente'

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS pacientes (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT NOT NULL,
            historial_medico TEXT,
            id_enfermero TEXT,
            id_medico TEXT,
            id_habitacion TEXT,
            rol TEXT NOT NULL DEFAULT 'paciente',
            FOREIGN KEY(id_enfermero) REFERENCES enfermeros(id) ON DELETE SET NULL,
            FOREIGN KEY(id_medico) REFERENCES medicos(id) ON DELETE SET NULL,
            FOREIGN KEY(id_habitacion) REFERENCES habitaciones(numero_habitacion) ON DELETE SET NULL
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_paciente(
    paciente_id: str,
    username: str,
    password: str,
    nombre: str,
    apellido: str,
    edad: int,
    genero: str,
    estado: str,
    historial_medico: Optional[List[str]] = None,
    id_enfermero: Optional[str] = None,
    id_medico: Optional[str] = None,
    id_habitacion: Optional[str] = None
) -> None:
    """
    Inserta un nuevo paciente en la tabla 'pacientes'.

    Parameters
    ----------
    paciente_id : str
        Identificador único del paciente.
    username : str
        Nombre de usuario único.
    password : str
        Contraseña.
    nombre : str
        Nombre de la persona.
    apellido : str
        Apellido de la persona.
    edad : int
        Edad de la persona.
    genero : str
        Género de la persona.
    estado : str
        Estado de salud del paciente.
    historial_medico : List[str], optional
        Lista de entradas de historial; por defecto None.
    id_enfermero : str, optional
        ID del enfermero asignado.
    id_medico : str, optional
        ID del médico asignado.
    id_habitacion : str, optional
        Número de habitación asignada.

    Raises
    ------
    ValueError
        Si la inserción viola restricciones de integridad.

    Returns
    -------
    None
    """
    historial_str = json.dumps(historial_medico) if historial_medico is not None else None
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pacientes (id, username, password, nombre, apellido, edad, genero, estado, historial_medico, id_enfermero, id_medico, id_habitacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (paciente_id, username, password, nombre, apellido, edad, genero, estado, historial_str, id_enfermero, id_medico, id_habitacion)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar paciente: {e}")
    finally:
        conn.close()


def leer_pacientes() -> List[Tuple[str, str, str, str, str, int, str, str, Optional[str], Optional[str], Optional[str], Optional[str], str]]:
    """
    Recupera todos los pacientes almacenados.

    Returns
    -------
    List[Tuple]
        Tuplas con campos en el orden definido en la tabla.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password, nombre, apellido, edad, genero, estado, historial_medico, id_enfermero, id_medico, id_habitacion, rol FROM pacientes;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_paciente(paciente_id: str) -> None:
    """
    Elimina un paciente de la base de datos por su identificador.

    Parameters
    ----------
    paciente_id : str
        Identificador del paciente a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM pacientes WHERE id = ?;",
        (paciente_id,)
    )
    conn.commit()
    conn.close()


def crear_tabla_paciente_enfermedad() -> None:
    """
    Crea la tabla 'paciente_enfermedad' en la base de datos si no existe.

    Relaciona pacientes con enfermedades (N:N).

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS paciente_enfermedad (
            paciente_id TEXT NOT NULL,
            enfermedad_id TEXT NOT NULL,
            PRIMARY KEY (paciente_id, enfermedad_id),
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
            FOREIGN KEY(enfermedad_id) REFERENCES enfermedades(id) ON DELETE CASCADE
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_paciente_enfermedad(paciente_id: str, enfermedad_id: str) -> None:
    """
    Asocia un paciente con una enfermedad.

    Parameters
    ----------
    paciente_id : str
    enfermedad_id : str

    Raises
    ------
    ValueError

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO paciente_enfermedad (paciente_id, enfermedad_id) VALUES (?, ?);",
            (paciente_id, enfermedad_id)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error al asociar paciente y enfermedad: {e}")
    finally:
        conn.close()


def leer_paciente_enfermedad() -> List[Tuple[str, str]]:
    """
    Recupera todas las asociaciones paciente-enfermedad.

    Returns
    -------
    List[Tuple[str, str]]
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT paciente_id, enfermedad_id FROM paciente_enfermedad;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_paciente_enfermedad(paciente_id: str, enfermedad_id: str) -> None:
    """
    Elimina una asociación paciente-enfermedad.

    Parameters
    ----------
    paciente_id : str
    enfermedad_id : str

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM paciente_enfermedad WHERE paciente_id = ? AND enfermedad_id = ?;",
        (paciente_id, enfermedad_id)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_pacientes()
    crear_tabla_paciente_enfermedad()
