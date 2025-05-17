import sqlite3


def conectar() -> sqlite3.Connection:
    """
    Establece la conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión a la base de datos.
    """
    return sqlite3.connect('../base_de_datos.db')


def crear_tabla_provincias() -> None:
    """
    Crea la tabla 'provincias' si no existe en la base de datos.

    La tabla almacena información sobre provincias, incluyendo
    el nombre de la comunidad a la que pertenece y su presupuesto.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS provincias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_comunidad TEXT NOT NULL,
            nombre_provincia TEXT NOT NULL UNIQUE,
            presupuesto REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'provincias' creada correctamente.")


def insertar_provincia(nombre_comunidad: str, nombre_provincia: str, presupuesto: float = 0) -> None:
    """
    Inserta una nueva provincia en la tabla.

    Parámetros
    ----------
    nombre_comunidad : str
        Nombre de la comunidad autónoma a la que pertenece la provincia.
    nombre_provincia : str
        Nombre de la provincia que se desea registrar.
    presupuesto : float, opcional
        Presupuesto inicial asignado a la provincia. Por defecto es 0.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO provincias (
                nombre_comunidad, nombre_provincia, presupuesto
            ) VALUES (?, ?, ?)
        ''', (nombre_comunidad, nombre_provincia, presupuesto))
        conn.commit()
        print(f"Provincia '{nombre_provincia}' insertada correctamente.")
    except sqlite3.IntegrityError:
        print("Error: La provincia ya está registrada.")
    finally:
        conn.close()


def leer_provincias() -> list:
    """
    Recupera todas las provincias almacenadas en la tabla.

    Devuelve
    --------
    list
        Lista de tuplas con la información de cada provincia.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM provincias")
    provincias = cursor.fetchall()
    conn.close()
    return provincias


def eliminar_provincia(nombre_provincia: str) -> None:
    """
    Elimina una provincia de la base de datos por su nombre.

    Parámetros
    ----------
    nombre_provincia : str
        Nombre de la provincia que se desea eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM provincias WHERE nombre_provincia = ?", (nombre_provincia,))
    conn.commit()
    conn.close()
    print(f"Provincia '{nombre_provincia}' eliminada.")


if __name__ == "__main__":
    crear_tabla_provincias()