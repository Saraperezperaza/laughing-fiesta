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

def crear_tabla_medicos() -> None:
    """
    Crea la tabla 'medicos' con herencia real desde 'trabajadores'.

    Contiene solo la información adicional de los médicos,
    como credenciales de acceso y especialización médica.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicos (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            antiguedad INTEGER NOT NULL,
            FOREIGN KEY (id) REFERENCES trabajadores(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'medicos' creada correctamente.")

def insertar_medico(
    id: str, username: str, password: str,
    especialidad: str, antiguedad: int
) -> None:
    """
    Inserta un nuevo médico en la tabla 'medicos'.

    La persona y el trabajador deben haberse registrado antes en las tablas correspondientes.

    Parámetros
    ----------
    id : str
        Identificador del médico (ya debe existir en 'trabajadores').
    username : str
        Nombre de usuario único del médico.
    password : str
        Contraseña del médico.
    especialidad : str
        Especialidad médica del profesional.
    antiguedad : int
        Años de experiencia del médico.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medicos (
                id, username, password, especialidad, antiguedad
            ) VALUES (?, ?, ?, ?, ?)
        ''', (id, username, password, especialidad, antiguedad))
        conn.commit()
        print(f"Médico con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: ID no existe en trabajadores o username ya está registrado.")
    finally:
        conn.close()

def leer_medicos() -> list:
    """
    Recupera todos los médicos registrados junto con sus atributos.

    Devuelve
    --------
    list
        Lista de tuplas con los datos de cada médico.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicos")
    medicos = cursor.fetchall()
    conn.close()
    return medicos

def actualizar_medico(id: str, campo: str, nuevo_valor) -> None:
    """
    Actualiza un campo específico de un médico.

    Parámetros
    ----------
    id : str
        ID del médico que se desea actualizar.
    campo : str
        Campo a modificar ('username', 'password', 'especialidad', 'antiguedad').
    nuevo_valor : str | int
        Nuevo valor del campo.
    """
    conn = conectar()
    cursor = conn.cursor()
    query = f"UPDATE medicos SET {campo} = ? WHERE id = ?"
    cursor.execute(query, (nuevo_valor, id))
    conn.commit()
    conn.close()
    print(f"Médico {id} actualizado correctamente: {campo} = {nuevo_valor}")

def eliminar_medico(id: str) -> None:
    """
    Elimina un médico de la tabla 'medicos' por su identificador.

    Parámetros
    ----------
    id : str
        Identificador del médico.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Médico {id} eliminado.")

if __name__ == "__main__":
    crear_tabla_medicos()

