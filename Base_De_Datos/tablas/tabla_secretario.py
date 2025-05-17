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


def crear_tabla_secretarios() -> None:
    """
    Crea la tabla 'secretarios', que hereda de la tabla 'trabajadores'.

    Esta tabla contiene únicamente los campos específicos de los secretarios.
    La información general está en 'personas' y 'trabajadores'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secretarios (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            email TEXT NOT NULL,
            departamento TEXT NOT NULL,
            FOREIGN KEY (id) REFERENCES trabajadores(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'secretarios' creada correctamente.")


def insertar_secretario(
    id: str,
    titulo: str,
    descripcion: str,
    antiguedad: int,
    email: str,
    departamento: str
) -> None:
    """
    Inserta un nuevo secretario en la tabla 'secretarios'.

    La persona debe haber sido registrada previamente en 'personas' y 'trabajadores'.

    Parámetros
    ----------
    id : str
        Identificador único del secretario (ya debe existir en 'trabajadores').
    titulo : str
        Título académico o profesional.
    descripcion : str
        Descripción del rol o funciones administrativas.
    antiguedad : int
        Años de experiencia o servicio.
    email : str
        Dirección de correo electrónico.
    departamento : str
        Departamento al que pertenece el secretario.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO secretarios (
                id, titulo, descripcion, antiguedad, email, departamento
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, titulo, descripcion, antiguedad, email, departamento))
        conn.commit()
        print(f"Secretario/a con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: ID no existe en 'trabajadores' o ya está registrado como secretario.")
    finally:
        conn.close()


def leer_secretarios() -> list:
    """
    Recupera todos los registros de la tabla 'secretarios'.

    Devuelve
    --------
    list
        Lista de tuplas con los datos de los secretarios.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM secretarios")
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def eliminar_secretario(id: str) -> None:
    """
    Elimina un secretario según su identificador.

    Parámetros
    ----------
    id : str
        Identificador único del secretario.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM secretarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Secretario/a con ID '{id}' eliminado.")


if __name__ == "__main__":
    crear_tabla_secretarios()
