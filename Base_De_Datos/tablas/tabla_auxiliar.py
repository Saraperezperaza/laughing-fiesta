import sqlite3
import json
import os

# Construir ruta absoluta al fichero de base de datos
base = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(base, 'base_de_datos.db')

def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Conexión activa al archivo de base de datos.
    """
    conn = sqlite3.connect(db_path)
    # Habilitar claves foráneas
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def crear_tabla_auxiliares() -> None:
    """
    Crea la tabla 'auxiliares' en la base de datos si no existe.

    Esta tabla hereda de 'trabajadores' a través de una clave foránea en la columna 'id'.
    Incluye además una relación 1:1 con la tabla 'enfermeros' mediante 'id_enfermero'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auxiliares (
            id TEXT PRIMARY KEY,
            antiguedad INTEGER NOT NULL,
            id_enfermero TEXT UNIQUE,
            rol TEXT DEFAULT 'auxiliar',
            FOREIGN KEY (id) REFERENCES trabajadores(id) ON DELETE CASCADE,
            FOREIGN KEY (id_enfermero) REFERENCES enfermeros(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'auxiliares' creada correctamente.")

def insertar_auxiliar(
    id: str,
    antiguedad: int,
    id_enfermero: str = None,
    rol: str = 'auxiliar'
) -> None:
    """
    Inserta un nuevo auxiliar en la tabla 'auxiliares'. Requiere que exista previamente en 'trabajadores'.

    Parámetros
    ----------
    id : str
        Identificador único del auxiliar, debe existir ya en la tabla 'trabajadores'.
    antiguedad : int
        Años de antigüedad del auxiliar.
    id_enfermero : str, opcional
        ID del enfermero asociado (relación 1:1).
    rol : str, opcional
        Rol del auxiliar en el sistema. Por defecto 'auxiliar'.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute('''
            INSERT INTO auxiliares (
                id, antiguedad, id_enfermero, rol
            ) VALUES (?, ?, ?, ?)
        ''', (id, antiguedad, id_enfermero, rol))
        conn.commit()
        print(f"Auxiliar '{id}' insertado correctamente.")
    except sqlite3.IntegrityError as e:
        print("Error de integridad:", e)
    finally:
        conn.close()

def leer_auxiliares() -> list[tuple]:
    """
    Recupera todos los auxiliares registrados.

    Devuelve
    -------
    list[tuple]
        Lista de auxiliares, incluyendo sus campos propios.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auxiliares")
    datos = cursor.fetchall()
    conn.close()
    return datos

def eliminar_auxiliar(id: str) -> None:
    """
    Elimina un auxiliar por su identificador.

    Parámetros
    ----------
    id : str
        Identificador del auxiliar a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auxiliares WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Auxiliar {id} eliminado correctamente.")

if __name__ == "__main__":
    crear_tabla_auxiliares()

