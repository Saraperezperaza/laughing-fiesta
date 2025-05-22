import sqlite3
import os
from typing import List, Tuple, Optional

# Base de datos en la misma carpeta que este script
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bdd.db')


def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite.

    Returns
    -------
    sqlite3.Connection
        Conexión activa al archivo de base de datos.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def crear_tabla_ambulancias() -> None:
    """
    Crea la tabla 'ambulancias' en la base de datos si no existe.

    La tabla contiene los siguientes campos (sin claves foráneas):
    - matricula : TEXT PRIMARY KEY
    - zona       : TEXT NOT NULL
    - modelo     : TEXT NOT NULL
    - sirena     : TEXT NOT NULL, restricción IN ('bitonal','secuencial')
    - id_centro  : TEXT NOT NULL

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ambulancias;")
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS ambulancias (
            matricula TEXT PRIMARY KEY,
            zona TEXT NOT NULL,
            modelo TEXT NOT NULL,
            sirena TEXT NOT NULL CHECK(sirena IN ('bitonal','secuencial')),
            id_centro TEXT NOT NULL,
            FOREIGN KEY (id_centro) REFERENCES centros(id_centro) ON DELETE CASCADE
        );
        '''
    )
    conn.commit()
    conn.close()


def insertar_ambulancia(
    matricula: str,
    zona: str,
    modelo: str,
    sirena: str,
    id_centro: str
) -> None:
    """
    Inserta una nueva ambulancia en la base de datos.

    Parameters
    ----------
    matricula : str
        Matrícula única de la ambulancia.
    zona : str
        Zona asignada a la ambulancia.
    modelo : str
        Modelo del vehículo.
    sirena : str
        Tipo de sirena ('bitonal' o 'secuencial').
    id_centro : str
        Identificador del centro asociado.

    Raises
    ------
    ValueError
        Si falla la integridad de la inserción.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ambulancias (matricula, zona, modelo, sirena, id_centro) VALUES (?, ?, ?, ?, ?);",
            (matricula, zona, modelo, sirena, id_centro)
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error de integridad al insertar ambulancia: {e}")
    finally:
        conn.close()


def leer_ambulancias() -> List[Tuple[str, str, str, str, str]]:
    """
    Recupera todas las ambulancias registradas.

    Returns
    -------
    List[Tuple[str, str, str, str, str]]
        Tuplas con campos:
        (matricula, zona, modelo, sirena, id_centro).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT matricula, zona, modelo, sirena, id_centro FROM ambulancias;"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_ambulancia(
    matricula: str,
    nueva_zona: Optional[str] = None,
    nuevo_modelo: Optional[str] = None,
    nueva_sirena: Optional[str] = None,
    nuevo_id_centro: Optional[str] = None
) -> None:
    """
    Actualiza los datos de una ambulancia existente.

    Parameters
    ----------
    matricula : str
        Matrícula de la ambulancia.
    nueva_zona : Optional[str]
        Nueva zona asignada.
    nuevo_modelo : Optional[str]
        Nuevo modelo del vehículo.
    nueva_sirena : Optional[str]
        Nuevo tipo de sirena.
    nuevo_id_centro : Optional[str]
        Nuevo identificador de centro.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    if nueva_zona is not None:
        cursor.execute(
            "UPDATE ambulancias SET zona = ? WHERE matricula = ?;",
            (nueva_zona, matricula)
        )
    if nuevo_modelo is not None:
        cursor.execute(
            "UPDATE ambulancias SET modelo = ? WHERE matricula = ?;",
            (nuevo_modelo, matricula)
        )
    if nueva_sirena is not None:
        cursor.execute(
            "UPDATE ambulancias SET sirena = ? WHERE matricula = ?;",
            (nueva_sirena, matricula)
        )
    if nuevo_id_centro is not None:
        cursor.execute(
            "UPDATE ambulancias SET id_centro = ? WHERE matricula = ?;",
            (nuevo_id_centro, matricula)
        )
    conn.commit()
    conn.close()


def eliminar_ambulancia(matricula: str) -> None:
    """
    Elimina una ambulancia de la base de datos por su matrícula.

    Parameters
    ----------
    matricula : str
        Matrícula de la ambulancia a eliminar.

    Returns
    -------
    None
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ambulancias WHERE matricula = ?;', (matricula,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_tabla_ambulancias()


