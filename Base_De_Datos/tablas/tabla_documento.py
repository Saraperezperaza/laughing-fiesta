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


def crear_tabla_documentos() -> None:
    """
    Crea la tabla 'documentos' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - id : TEXT PRIMARY KEY
    - titulo : TEXT NOT NULL
    - descripcion : TEXT NOT NULL
    - urgente : INTEGER NOT NULL DEFAULT 0
    - prioridad : INTEGER NOT NULL DEFAULT 0 CHECK(prioridad IN (0, 1))
    - id_secretario : TEXT

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS documentos (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            urgente INTEGER NOT NULL DEFAULT 0,
            prioridad INTEGER NOT NULL DEFAULT 0 CHECK (prioridad IN (0, 1)),
            id_secretario TEXT,
            FOREIGN KEY(id_secretario) REFERENCES secretarios(id) ON DELETE SET NULL
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_documento(
    doc_id: str,
    titulo: str,
    descripcion: str,
    urgente: bool = False,
    prioridad: int = 0
) -> None:
    """
    Inserta un nuevo documento en la tabla 'documentos'.

    Parameters
    ----------
    doc_id : str
        Identificador único del documento.
    titulo : str
        Título del documento.
    descripcion : str
        Descripción o contenido del documento.
    urgente : bool, optional
        Indicador de urgencia; por defecto False.
    prioridad : int, optional
        Nivel de prioridad (0: normal, 1: urgente); por defecto 0.

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
            "INSERT INTO documentos (id, titulo, descripcion, urgente, prioridad) VALUES (?, ?, ?, ?, ?);",
            (doc_id, titulo, descripcion, int(urgente), prioridad)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar documento: {e}")
    finally:
        conn.close()


def leer_documentos() -> List[Tuple[str, str, str, int, int, str]]:
    """
    Recupera todos los documentos almacenados en la base de datos.

    Returns
    -------
    List[Tuple[str, str, str, int, int, str]]
        Tuplas con campos:
        (id, titulo, descripcion, urgente, prioridad, id_secretario).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, descripcion, urgente, prioridad, id_secretario FROM documentos;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def marcar_documento_urgente(doc_id: str) -> None:
    """
    Marca un documento como urgente, actualizando 'urgente' y 'prioridad'.

    Parameters
    ----------
    doc_id : str
        Identificador del documento a actualizar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE documentos SET urgente = 1, prioridad = 1 WHERE id = ?;",
        (doc_id,)
    )
    conn.commit()
    conn.close()


def eliminar_documento(doc_id: str) -> None:
    """
    Elimina un documento de la base de datos por su identificador.

    Parameters
    ----------
    doc_id : str
        Identificador único del documento a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM documentos WHERE id = ?;', (doc_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_documentos()


