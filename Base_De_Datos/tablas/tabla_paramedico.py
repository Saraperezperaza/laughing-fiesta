import sqlite3

def conectar():
    """
    Establece la conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión a la base de datos.
    """
    return sqlite3.connect('../base_de_datos.db')


def crear_tabla_paramedicos() -> None:
    """
    Crea la tabla 'paramedicos' con herencia desde 'trabajadores'.

    La tabla almacena solo información específica de los paramédicos y
    se relaciona con 'trabajadores' mediante la clave foránea 'id'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paramedicos (
            id TEXT PRIMARY KEY,
            especialidad TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            id_ambulancia TEXT,
            FOREIGN KEY (id) REFERENCES trabajadores(id) ON DELETE CASCADE,
            FOREIGN KEY (id_ambulancia) REFERENCES ambulancias(matricula)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'paramedicos' creada correctamente.")


def insertar_paramedico(
    id: str,
    especialidad: str,
    antiguedad: int,
    id_ambulancia: str = None
) -> None:
    """
    Inserta un nuevo paramédico en la base de datos.

    Requiere que la persona ya esté en 'personas' y 'trabajadores'.

    Parámetros
    ----------
    id : str
        Identificador único (ya debe existir en 'trabajadores').
    especialidad : str
        Especialidad médica del paramédico.
    antiguedad : int
        Años de experiencia.
    id_ambulancia : str, opcional
        Matrícula de la ambulancia asignada.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO paramedicos (
                id, especialidad, antiguedad, id_ambulancia
            ) VALUES (?, ?, ?, ?)
        ''', (id, especialidad, antiguedad, id_ambulancia))
        conn.commit()
        print(f"Paramédico con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError as e:
        print("Error de integridad:", e)
    finally:
        conn.close()


def leer_paramedicos() -> list:
    """
    Recupera todos los paramédicos registrados.

    Devuelve
    --------
    list
        Lista de tuplas con los datos específicos de los paramédicos.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paramedicos")
    paramedicos = cursor.fetchall()
    conn.close()
    return paramedicos


def eliminar_paramedico(id: str) -> None:
    """
    Elimina un paramédico de la base de datos según su ID.

    Parámetros
    ----------
    id : str
        Identificador del paramédico.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paramedicos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Paramédico {id} eliminado.")


if __name__ == "__main__":
    crear_tabla_paramedicos()


