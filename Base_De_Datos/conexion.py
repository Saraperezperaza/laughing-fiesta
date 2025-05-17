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
