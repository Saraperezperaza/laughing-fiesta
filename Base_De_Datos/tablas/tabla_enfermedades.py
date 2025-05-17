import sqlite3

def conectar():
    """
    Establece una conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión a la base de datos 'base_de_datos.db'.
    """
    return sqlite3.connect('../base_de_datos.db')

def crear_tabla_enfermedades():
    """
    Crea la tabla 'enfermedades' si no existe ya en la base de datos.

    La tabla almacena información sobre cada enfermedad:
    - id: clave primaria única.
    - nombre: nombre de la enfermedad.
    - sintomas: descripción textual de los síntomas.
    - cronica: indica si la enfermedad es crónica (0 o 1).
    - grave: indica si la enfermedad es grave (0 o 1).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enfermedades (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            sintomas TEXT NOT NULL,
            cronica INTEGER DEFAULT 0,
            grave INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'enfermedades' creada correctamente.")

def insertar_enfermedad(id: str, nombre: str, sintomas: str, cronica: bool = False, grave: bool = False):
    """
    Inserta una nueva enfermedad en la tabla.

    Parámetros
    ----------
    id : str
        Identificador único de la enfermedad.
    nombre : str
        Nombre de la enfermedad.
    sintomas : str
        Descripción de los síntomas asociados.
    cronica : bool, opcional
        Indica si la enfermedad es crónica (por defecto False).
    grave : bool, opcional
        Indica si la enfermedad es grave (por defecto False).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO enfermedades (
                id, nombre, sintomas, cronica, grave
            ) VALUES (?, ?, ?, ?, ?)
        ''', (id, nombre, sintomas, int(cronica), int(grave)))
        conn.commit()
        print(f"Enfermedad '{nombre}' insertada correctamente.")
    except sqlite3.IntegrityError:
        print("Error: El ID ya existe.")
    finally:
        conn.close()

def leer_enfermedades():
    """
    Recupera todos los registros de la tabla 'enfermedades'.

    Devuelve
    --------
    list of tuple
        Lista con las enfermedades almacenadas en la base de datos.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enfermedades")
    enfermedades = cursor.fetchall()
    conn.close()
    return enfermedades

def marcar_enfermedad_grave(id: str):
    """
    Marca una enfermedad como grave en la base de datos.

    Parámetros
    ----------
    id : str
        Identificador único de la enfermedad a modificar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE enfermedades SET grave = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Enfermedad {id} marcada como grave.")

def eliminar_enfermedad(id: str):
    """
    Elimina una enfermedad de la base de datos.

    Parámetros
    ----------
    id : str
        Identificador único de la enfermedad a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enfermedades WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Enfermedad {id} eliminada.")

if __name__ == "__main__":
    crear_tabla_enfermedades()
