import sqlite3
import os
from typing import List, Tuple

# Base de datos en la misma carpeta que este script
_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdd.db')

def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite y habilita claves foráneas.

    Returns
    -------
    sqlite3.Connection
        Conexión activa al archivo de base de datos.
    """
    conn = sqlite3.connect(_db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def crear_tabla_asignaciones() -> None:
    """
    Crea la tabla 'asignaciones' si no existe.

    La tabla vincula pacientes con médicos:
    - id            : INTEGER PRIMARY KEY AUTOINCREMENT
    - paciente_id   : TEXT NOT NULL, FK -> pacientes(id)
    - medico_id     : TEXT NOT NULL, FK -> medicos(id)

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS asignaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id TEXT NOT NULL,
            medico_id TEXT NOT NULL,
            id_enfermero TEXT NOT NULL,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
            FOREIGN KEY(medico_id) REFERENCES medicos(id)   ON DELETE CASCADE,
            FOREIGN KEY (id_enfermero) REFERENCES enfermeros(id) ON DELETE CASCADE
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_asignacion(paciente_id: str, medico_id: str) -> None:
    """
    Inserta una nueva asignación paciente–médico.

    Parameters
    ----------
    paciente_id : str
        Identificador del paciente.
    medico_id : str
        Identificador del médico.

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
            "INSERT INTO asignaciones (paciente_id, medico_id) VALUES (?, ?);",
            (paciente_id, medico_id)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error al insertar asignación: {e}")
    finally:
        conn.close()


def leer_asignaciones() -> List[Tuple[int, str, str]]:
    """
    Recupera todas las asignaciones de pacientes a médicos.

    Returns
    -------
    List[Tuple[int, str, str]]
        Tuplas con campos:
        (id, paciente_id, medico_id).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, paciente_id, medico_id FROM asignaciones;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_asignacion(asignacion_id: int) -> None:
    """
    Elimina una asignación por su identificador.

    Parameters
    ----------
    asignacion_id : int
        ID de la asignación a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM asignaciones WHERE id = ?;",
        (asignacion_id,)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_asignaciones()
