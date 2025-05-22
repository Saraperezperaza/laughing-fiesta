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


def crear_tabla_secretarios() -> None:
    """
    Crea la tabla 'secretarios' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único del secretario (clave primaria).
    - titulo : TEXT
        Título académico o profesional.
    - descripcion : TEXT
        Descripción de funciones administrativas.
    - antiguedad : INTEGER
        Años de experiencia o servicio.
    - email : TEXT
        Dirección de correo electrónico.
    - departamento : TEXT
        Departamento al que pertenece.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS secretarios (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            email TEXT NOT NULL,
            departamento TEXT NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_secretario(
    secretario_id: str,
    titulo: str,
    descripcion: str,
    antiguedad: int,
    email: str,
    departamento: str
) -> None:
    """
    Inserta un nuevo secretario en la tabla 'secretarios'.

    Parameters
    ----------
    secretario_id : str
        Identificador único del secretario.
    titulo : str
        Título académico o profesional.
    descripcion : str
        Descripción de funciones.
    antiguedad : int
        Años de experiencia.
    email : str
        Correo electrónico.
    departamento : str
        Departamento asociado.

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
            "INSERT INTO secretarios (id, titulo, descripcion, antiguedad, email, departamento) VALUES (?, ?, ?, ?, ?, ?);",
            (secretario_id, titulo, descripcion, antiguedad, email, departamento)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar secretario: {e}")
    finally:
        conn.close()


def leer_secretarios() -> List[Tuple[str, str, str, int, str, str]]:
    """
    Recupera todos los secretarios almacenados.

    Returns
    -------
    List[Tuple[str, str, str, int, str, str]]
        Tuplas con campos:
        (id, titulo, descripcion, antiguedad, email, departamento).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, antiguedad, email, departamento FROM secretarios;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_secretario(secretario_id: str) -> None:
    """
    Elimina un secretario de la base de datos por su identificador.

    Parameters
    ----------
    secretario_id : str
        Identificador del secretario a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM secretarios WHERE id = ?;",
        (secretario_id,)
    )
    conn.commit()
    conn.close()


def crear_tabla_trabajadores() -> None:
    """
    Crea la tabla 'trabajadores' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT
        Identificador único del trabajador (clave primaria).
    - turno : TEXT
        Turno laboral ('mañana', 'tarde', 'noche').
    - horas : INTEGER
        Horas trabajadas por semana.
    - salario : REAL
        Salario mensual.
    - rol : TEXT
        Rol en el sistema; por defecto 'trabajador'.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS trabajadores (
            id TEXT PRIMARY KEY,
            turno TEXT NOT NULL,
            horas INTEGER NOT NULL,
            salario REAL NOT NULL,
            rol TEXT NOT NULL DEFAULT 'trabajador'
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_trabajador(
    trabajador_id: str,
    turno: str,
    horas: int,
    salario: float,
    rol: str = 'trabajador'
) -> None:
    """
    Inserta un nuevo trabajador en la tabla 'trabajadores'.

    Parameters
    ----------
    trabajador_id : str
        Identificador único del trabajador.
    turno : str
        Turno asignado.
    horas : int
        Horas trabajadas por semana.
    salario : float
        Salario mensual.
    rol : str, optional
        Rol en el sistema; por defecto 'trabajador'.

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
            "INSERT INTO trabajadores (id, turno, horas, salario, rol) VALUES (?, ?, ?, ?, ?);",
            (trabajador_id, turno, horas, salario, rol)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar trabajador: {e}")
    finally:
        conn.close()


def leer_trabajadores() -> List[Tuple[str, str, int, float, str]]:
    """
    Recupera todos los trabajadores almacenados.

    Returns
    -------
    List[Tuple[str, str, int, float, str]]
        Tuplas con campos:
        (id, turno, horas, salario, rol).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, turno, horas, salario, rol FROM trabajadores;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_trabajador(trabajador_id: str) -> None:
    """
    Elimina un trabajador de la base de datos por su identificador.

    Parameters
    ----------
    trabajador_id : str
        Identificador del trabajador a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM trabajadores WHERE id = ?;",
        (trabajador_id,)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_secretarios()
    crear_tabla_trabajadores()

