import sqlite3
import os
from typing import List, Optional

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


def crear_tabla_sip() -> None:
    """
    Crea la tabla 'SIPS' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - sip : TEXT PRIMARY KEY
    - paciente_id : TEXT NOT NULL (clave ajena a pacientes.id)
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS SIPS (
            sip TEXT PRIMARY KEY,
            paciente_id TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_sip(sip: str, paciente_id: str) -> None:
    """
    Inserta un nuevo SIP en la tabla 'SIPS'.

    Parameters
    ----------
    sip : str
        Identificador único del SIP.
    paciente_id : str
        Id del paciente al que pertenece el SIP.

    Raises
    ------
    ValueError
        Si la inserción viola restricciones de integridad.
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO SIPS (sip, paciente_id) VALUES (?, ?);",
            (sip, paciente_id)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar SIP: {e}")
    finally:
        conn.close()


def leer_sip(paciente_id: str) -> Optional[str]:
    """
    Recupera el SIP asociado a un paciente.

    Parameters
    ----------
    paciente_id : str
        Identificador del paciente.

    Returns
    -------
    Optional[str]
        SIP si existe, o None si no hay registro.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sip FROM SIPS WHERE paciente_id = ?;",
        (paciente_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def leer_todos_sips() -> List[tuple]:
    """
    Recupera todos los registros de la tabla SIPS.

    Returns
    -------
    List[tuple]
        Lista de tuplas (sip, paciente_id).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sip, paciente_id FROM SIPS;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_sip(paciente_id: str) -> None:
    """
    Elimina el SIP asociado a un paciente.

    Parameters
    ----------
    paciente_id : str
        Identificador del paciente cuyo SIP se va a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM SIPS WHERE paciente_id = ?;",
        (paciente_id,)
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_sip()