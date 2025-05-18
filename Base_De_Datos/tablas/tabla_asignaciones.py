import sqlite3
import os

base = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(base, 'base_de_datos.db')

def conectar() -> sqlite3.Connection:
    """
    Devuelve una conexión a la base de datos, con claves foráneas activadas.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def crear_tabla_asignaciones() -> None:
    """
    Crea la tabla 'asignaciones' si no existe.

    Almacena parejas paciente–médico.
    """
    sql = '''
    CREATE TABLE IF NOT EXISTS asignaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id TEXT NOT NULL,
        medico_id TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
        FOREIGN KEY (medico_id)   REFERENCES medicos(id)   ON DELETE CASCADE
    )
    '''
    conn = conectar()
    conn.execute(sql)
    conn.commit()
    conn.close()
