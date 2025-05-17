import sqlite3

def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión a la base de datos.
    """
    return sqlite3.connect('../base_de_datos.db')

def crear_tabla_personas() -> None:
    """
    Crea la tabla 'personas' en la base de datos si no existe.
    Esta tabla almacena información general de cualquier tipo de persona
    en el sistema: pacientes, médicos, enfermeros, etc.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            genero TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'personas' creada correctamente.")

def insertar_persona(id: str, nombre: str, apellido: str, edad: int,
                     genero: str, password_hash: str, rol: str) -> None:
    """
    Inserta una nueva persona en la tabla.

    Parámetros
    ----------
    id : str
        Identificador único de la persona.
    nombre : str
        Nombre de la persona.
    apellido : str
        Apellido de la persona.
    edad : int
        Edad de la persona.
    genero : str
        Género de la persona.
    password_hash : str
        Contraseña hasheada para mayor seguridad.
    rol : str
        Rol que desempeña la persona en el sistema (por ejemplo: paciente, médico, enfermero, etc.).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO personas (
                id, nombre, apellido, edad, genero, password_hash, rol
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id, nombre, apellido, edad, genero, password_hash, rol))
        conn.commit()
        print(f"Persona '{nombre} {apellido}' insertada correctamente.")
    except sqlite3.IntegrityError:
        print("Error: ID ya existe.")
    finally:
        conn.close()

def leer_personas() -> list:
    """
    Recupera todas las personas almacenadas en la tabla.

    Devuelve
    --------
    list
        Lista de tuplas con los datos de las personas.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    conn.close()
    return personas

def eliminar_persona(id: str) -> None:
    """
    Elimina una persona de la base de datos según su identificador.

    Parámetros
    ----------
    id : str
        Identificador único de la persona que se desea eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Persona {id} eliminada.")

if __name__ == "__main__":
    crear_tabla_personas()
