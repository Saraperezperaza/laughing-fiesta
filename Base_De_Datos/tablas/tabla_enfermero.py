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


def crear_tabla_enfermeros() -> None:
    """
    Crea la tabla 'enfermeros', heredando de 'trabajadores'.

    La relación se establece a través del campo 'id', que es clave foránea a 'trabajadores(id)'.
    La tabla almacena datos específicos de los enfermeros como especialidad, antigüedad, usuario y contraseña.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enfermeros (
            id TEXT PRIMARY KEY,
            especialidad TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT DEFAULT 'enfermero',
            FOREIGN KEY (id) REFERENCES trabajadores(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'enfermeros' creada correctamente.")


def insertar_enfermero(
    id: str,
    especialidad: str,
    antiguedad: int,
    username: str,
    password: str,
    rol: str = 'enfermero'
) -> None:
    """
    Inserta un nuevo enfermero en la tabla 'enfermeros'.

    Parámetros
    ----------
    id : str
        Identificador del enfermero (debe existir previamente en 'trabajadores').
    especialidad : str
        Especialidad médica del enfermero.
    antiguedad : int
        Años de experiencia laboral.
    username : str
        Nombre de usuario único.
    password : str
        Contraseña (preferiblemente encriptada).
    rol : str, opcional
        Rol asignado, por defecto 'enfermero'.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute('''
            INSERT INTO enfermeros (
                id, especialidad, antiguedad, username, password, rol
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, especialidad, antiguedad, username, password, rol))
        conn.commit()
        print(f"Enfermero con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: El ID no existe en trabajadores o el username ya está en uso.")
    finally:
        conn.close()


def leer_enfermeros() -> list:
    """
    Recupera todos los enfermeros registrados en la tabla.

    Devuelve
    --------
    list
        Lista de tuplas con los datos de cada enfermero.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enfermeros")
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_enfermero(id: str, campo: str, nuevo_valor) -> None:
    """
    Actualiza un campo específico de un enfermero.

    Parámetros
    ----------
    id : str
        Identificador del enfermero.
    campo : str
        Nombre del campo a modificar.
    nuevo_valor : Any
        Nuevo valor para el campo.
    """
    conn = conectar()
    cursor = conn.cursor()
    query = f"UPDATE enfermeros SET {campo} = ? WHERE id = ?"
    cursor.execute(query, (nuevo_valor, id))
    conn.commit()
    conn.close()
    print(f"Enfermero {id} actualizado: {campo} = {nuevo_valor}")


def eliminar_enfermero(id: str) -> None:
    """
    Elimina un enfermero de la base de datos.

    Parámetros
    ----------
    id : str
        Identificador único del enfermero.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enfermeros WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Enfermero {id} eliminado.")


if __name__ == "__main__":
    crear_tabla_enfermeros()

