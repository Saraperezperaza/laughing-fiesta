import sqlite3

def conectar():
    """
    Establece una conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión activo con la base de datos 'base_de_datos.db'.
    """
    return sqlite3.connect('../base_de_datos.db')

def crear_tabla_documentos():
    """
    Crea la tabla 'documentos' si no existe ya en la base de datos.

    La tabla incluye los siguientes campos:
    - id: clave primaria del documento.
    - titulo: título del documento.
    - descripcion: contenido o resumen del documento.
    - urgente: indicador booleano de urgencia.
    - prioridad: nivel de prioridad (0: normal, 1: urgente).
    - id_secretario: clave foránea que relaciona el documento con un secretario.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            urgente BOOLEAN NOT NULL DEFAULT 0,
            prioridad INTEGER NOT NULL DEFAULT 0 CHECK (prioridad IN (0, 1)),
            id_secretario TEXT,
            FOREIGN KEY (id_secretario) REFERENCES secretarios(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'documentos' creada correctamente.")

def insertar_documento(
    id: str,
    titulo: str,
    descripcion: str,
    urgente: bool = False,
    prioridad: int = 0
):
    """
    Inserta un nuevo documento en la tabla.

    Parámetros
    ----------
    id : str
        Identificador único del documento.
    titulo : str
        Título del documento.
    descripcion : str
        Descripción o contenido del documento.
    urgente : bool, opcional
        Si el documento es urgente (por defecto False).
    prioridad : int, opcional
        Nivel de prioridad (0: normal, 1: urgente).
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documentos (
                id, titulo, descripcion, urgente, prioridad
            ) VALUES (?, ?, ?, ?, ?)
        ''', (id, titulo, descripcion, int(urgente), prioridad))
        conn.commit()
        print(f"Documento '{titulo}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: El ID ya existe.")
    finally:
        conn.close()

def leer_documentos():
    """
    Recupera todos los documentos almacenados en la base de datos.

    Devuelve
    --------
    Lista
        Lista con todas las filas de la tabla 'documentos'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documentos")
    documentos = cursor.fetchall()
    conn.close()
    return documentos

def marcar_documento_urgente(id: str):
    """
    Marca un documento como urgente, actualizando sus campos 'urgente' y 'prioridad'.

    Parámetros
    ----------
    id : str
        Identificador del documento a actualizar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE documentos
        SET urgente = 1, prioridad = 1
        WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()
    print(f"Documento {id} marcado como urgente.")

def eliminar_documento(id: str):
    """
    Elimina un documento de la base de datos según su identificador.

    Parámetros
    ----------
    id : str
        Identificador del documento a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Documento {id} eliminado.")

if __name__ == "__main__":
    crear_tabla_documentos()

