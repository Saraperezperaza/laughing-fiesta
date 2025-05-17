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

def crear_tabla_trabajadores() -> None:
    """
    Crea la tabla 'trabajadores', con herencia real desde la tabla 'personas'.

    Esta tabla solo almacena información laboral, el resto de datos personales
    se encuentran en la tabla 'personas' mediante una clave foránea.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trabajadores (
            id TEXT PRIMARY KEY,
            turno TEXT NOT NULL,
            horas INTEGER NOT NULL,
            salario REAL NOT NULL,
            rol TEXT DEFAULT 'trabajador',
            FOREIGN KEY (id) REFERENCES personas(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'trabajadores' creada correctamente.")

def insertar_trabajador(
    id: str, turno: str, horas: int, salario: float, rol: str = 'trabajador'
) -> None:
    """
    Inserta un nuevo trabajador en la tabla 'trabajadores'.

    Requiere que la persona ya haya sido registrada previamente en la tabla 'personas'.

    Parámetros
    ----------
    id : str
        Identificador único del trabajador (debe existir en 'personas').
    turno : str
        Turno laboral asignado (mañana, tarde, noche).
    horas : int
        Número de horas trabajadas por semana.
    salario : float
        Salario mensual.
    rol : str, opcional
        Rol en el sistema, por defecto es 'trabajador'.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trabajadores (
                id, turno, horas, salario, rol
            ) VALUES (?, ?, ?, ?, ?)
        ''', (id, turno, horas, salario, rol))
        conn.commit()
        print(f"Trabajador con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: el ID no existe en personas o ya está registrado como trabajador.")
    finally:
        conn.close()

def leer_trabajadores() -> list:
    """
    Recupera todos los trabajadores registrados.

    Devuelve
    --------
    list
        Lista de tuplas con los datos laborales de cada trabajador.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trabajadores")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def eliminar_trabajador(id: str) -> None:
    """
    Elimina un trabajador (solo su parte laboral, no la persona).

    Parámetros
    ----------
    id : str
        Identificador del trabajador a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trabajadores WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Trabajador con ID '{id}' eliminado.")

if __name__ == "__main__":
    crear_tabla_trabajadores()
