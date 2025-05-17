import sqlite3

def conectar():
    """
    Establece una conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión a la base de datos '../base_de_datos.db'.
    """
    return sqlite3.connect('../base_de_datos.db')

def crear_tabla_habitaciones() -> None:
    """
    Crea la tabla 'habitaciones' si no existe en la base de datos.

    La tabla contiene:
    - numero_habitacion: número único que identifica la habitación.
    - capacidad: número máximo de pacientes permitidos.
    - limpia: indica si la habitación está limpia (1) o no (0).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habitaciones (
            numero_habitacion INTEGER PRIMARY KEY,
            capacidad INTEGER NOT NULL,
            limpia INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'habitaciones' creada correctamente.")

def insertar_habitacion(numero_habitacion: int, capacidad: int, limpia: bool = False) -> None:
    """
    Inserta una nueva habitación en la tabla.

    Parámetros
    ----------
    numero_habitacion : int
        Identificador único de la habitación.
    capacidad : int
        Número máximo de pacientes que pueden alojarse.
    limpia : bool, opcional
        Estado de limpieza de la habitación (por defecto False).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO habitaciones (
                numero_habitacion, capacidad, limpia
            ) VALUES (?, ?, ?)
        ''', (numero_habitacion, capacidad, int(limpia)))
        conn.commit()
        print(f"Habitación {numero_habitacion} insertada correctamente.")
    except sqlite3.IntegrityError:
        print("Error: El número de habitación ya existe.")
    finally:
        conn.close()

def leer_habitaciones() -> list[tuple]:
    """
    Recupera todas las habitaciones registradas en la base de datos.

    Devuelve
    --------
    Lista
        Lista de tuplas con los datos de todas las habitaciones.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habitaciones")
    habitaciones = cursor.fetchall()
    conn.close()
    return habitaciones

def limpiar_habitacion(numero_habitacion: int) -> None:
    """
    Marca una habitación como limpia.

    Parámetros
    ----------
    numero_habitacion : int
        Número identificador de la habitación a actualizar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE habitaciones SET limpia = 1 WHERE numero_habitacion = ?
    ''', (numero_habitacion,))
    conn.commit()
    conn.close()
    print(f"Habitación {numero_habitacion} marcada como limpia.")

def eliminar_habitacion(numero_habitacion: int) -> None:
    """
    Elimina una habitación de la base de datos.

    Parámetros
    ----------
    numero_habitacion : int
        Número de habitación a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habitaciones WHERE numero_habitacion = ?", (numero_habitacion,))
    conn.commit()
    conn.close()
    print(f"Habitación {numero_habitacion} eliminada.")

if __name__ == "__main__":
    crear_tabla_habitaciones()
