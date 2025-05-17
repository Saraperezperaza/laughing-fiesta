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


def crear_tabla_centros():
    """
    Crea la tabla 'centros' si no existe ya en la base de datos.

    La tabla incluye una clave foránea 'id_provincia' que enlaza con la tabla 'provincias',
    simulando así una relación de herencia lógica.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS centros (
            id_centro TEXT PRIMARY KEY,
            nombre_centro TEXT NOT NULL,
            cantidad_trabajadores INTEGER NOT NULL,
            presupuesto REAL NOT NULL,
            habitaciones INTEGER NOT NULL,
            id_provincia INTEGER NOT NULL,
            FOREIGN KEY (id_provincia) REFERENCES provincias(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'centros' creada correctamente.")


def insertar_centro(id_centro: str, nombre_centro: str, cantidad_trabajadores: int,
                    presupuesto: float, habitaciones: int, id_provincia: int) -> None:
    """
    Inserta un nuevo centro médico en la base de datos.

    Parámetros
    ----------
    id_centro : str
        Identificador único del centro.
    nombre_centro : str
        Nombre del centro médico.
    cantidad_trabajadores : int
        Número de trabajadores en el centro.
    presupuesto : float
        Presupuesto asignado.
    habitaciones : int
        Número de habitaciones disponibles.
    id_provincia : int
        Identificador de la provincia relacionada.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('''
            INSERT INTO centros (
                id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones, id_provincia
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (id_centro, nombre_centro, cantidad_trabajadores, presupuesto, habitaciones, id_provincia))
        conn.commit()
        print(f"Centro '{nombre_centro}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: el ID ya existe o la provincia no es válida.")
    finally:
        conn.close()


def leer_centros() -> list[tuple]:
    """
    Recupera todos los registros de la tabla 'centros'.

    Devuelve
    --------
    list of tuple
        Lista de tuplas con los datos de todos los centros médicos.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM centros")
    centros = cursor.fetchall()
    conn.close()
    return centros


def actualizar_centro(id_centro: str, nuevo_nombre: str = None, nuevos_trabajadores: int = None,
                      nuevo_presupuesto: float = None, nueva_provincia: int = None) -> None:
    """
    Actualiza la información de un centro médico existente.

    Parámetros
    ----------
    id_centro : str
        ID del centro a modificar.
    nuevo_nombre : str, opcional
        Nuevo nombre del centro.
    nuevos_trabajadores : int, opcional
        Nueva cantidad de trabajadores.
    nuevo_presupuesto : float, opcional
        Nuevo presupuesto.
    nueva_provincia : int, opcional
        Nuevo ID de provincia al que se asigna el centro.
    """
    conn = conectar()
    cursor = conn.cursor()
    if nuevo_nombre:
        cursor.execute("UPDATE centros SET nombre_centro = ? WHERE id_centro = ?", (nuevo_nombre, id_centro))
    if nuevos_trabajadores:
        cursor.execute("UPDATE centros SET cantidad_trabajadores = ? WHERE id_centro = ?", (nuevos_trabajadores, id_centro))
    if nuevo_presupuesto:
        cursor.execute("UPDATE centros SET presupuesto = ? WHERE id_centro = ?", (nuevo_presupuesto, id_centro))
    if nueva_provincia:
        cursor.execute("UPDATE centros SET id_provincia = ? WHERE id_centro = ?", (nueva_provincia, id_centro))
    conn.commit()
    conn.close()
    print(f"Centro {id_centro} actualizado correctamente.")


def eliminar_centro(id_centro: str) -> None:
    """
    Elimina un centro de la base de datos.

    Parámetros
    ----------
    id_centro : str
        Identificador único del centro a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM centros WHERE id_centro = ?", (id_centro,))
    conn.commit()
    conn.close()
    print(f"Centro {id_centro} eliminado correctamente.")

if __name__ == "__main__":
    crear_tabla_centros()