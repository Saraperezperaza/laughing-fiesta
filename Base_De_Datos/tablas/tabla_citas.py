import sqlite3
import os
from typing import List, Tuple, Optional

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


def crear_tabla_citas() -> None:
    """
    Crea la tabla 'citas' en la base de datos si no existe.

    La tabla contiene los siguientes campos:

    - id_cita : TEXT PRIMARY KEY
    - paciente : TEXT NOT NULL
    - medico : TEXT NOT NULL
    - motivo : TEXT NOT NULL
    - fecha_hora : TEXT NOT NULL
    - estado : TEXT NOT NULL DEFAULT 'pendiente'
    - atendido : INTEGER NOT NULL DEFAULT 0

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS citas (
            id_cita TEXT PRIMARY KEY,
            paciente TEXT NOT NULL,
            medico TEXT NOT NULL,
            motivo TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            atendido INTEGER NOT NULL DEFAULT 0
        );
        '''
    )
    cursor.execute("SELECT * FROM pacientes")
    conn.commit()
    conn.close()


def insertar_cita(
    id_cita: str,
    paciente: str,
    medico: str,
    motivo: str,
    fecha_hora: str,
    estado: str = 'pendiente',
    atendido: bool = False
) -> None:
    """
    Inserta una nueva cita médica en la base de datos.

    Parameters
    ----------
    id_cita : str
        Identificador único de la cita.
    paciente : str
        Nombre o identificador del paciente.
    medico : str
        Nombre o identificador del médico.
    motivo : str
        Motivo de la cita.
    fecha_hora : str
        Fecha y hora de la cita en formato de texto.
    estado : str, optional
        Estado de la cita ('pendiente', 'completado', 'cancelado').
    atendido : bool, optional
        Indica si la cita ha sido atendida; por defecto False.

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
            "INSERT INTO citas (id_cita, paciente, medico, motivo, fecha_hora, estado, atendido) VALUES (?, ?, ?, ?, ?, ?, ?);",
            (id_cita, paciente, medico, motivo, fecha_hora, estado, int(atendido))
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar cita: {e}")
    finally:
        conn.close()


def leer_citas() -> List[Tuple[str, str, str, str, str, int, int]]:
    """
    Recupera todas las citas almacenadas en la base de datos.

    Returns
    -------
    List[Tuple[str, str, str, str, str, int, int]]
        Tuplas con campos:
        (id_cita, paciente, medico, motivo, fecha_hora, estado, atendido).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_cita, paciente, medico, motivo, fecha_hora, estado, atendido FROM citas;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_cita(
    id_cita: str,
    nuevo_estado: Optional[str] = None,
    atendido: Optional[bool] = None
) -> None:
    """
    Actualiza el estado y/o el indicador de atención de una cita existente.

    Parameters
    ----------
    id_cita : str
        Identificador de la cita a modificar.
    nuevo_estado : str, optional
        Nuevo estado de la cita ('pendiente', 'completado', 'cancelado').
    atendido : bool, optional
        Nuevo valor para el campo 'atendido'.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    if nuevo_estado is not None:
        cursor.execute(
            "UPDATE citas SET estado = ? WHERE id_cita = ?;",
            (nuevo_estado, id_cita)
        )
    if atendido is not None:
        cursor.execute(
            "UPDATE citas SET atendido = ? WHERE id_cita = ?;",
            (int(atendido), id_cita)
        )
    conn.commit()
    conn.close()


def eliminar_cita(id_cita: str) -> None:
    """
    Elimina una cita de la base de datos según su identificador.

    Parameters
    ----------
    id_cita : str
        Identificador único de la cita a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM citas WHERE id_cita = ?;', (id_cita,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_citas()