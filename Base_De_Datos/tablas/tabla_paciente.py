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
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def crear_tabla_pacientes() -> None:
    """
    Crea la tabla 'pacientes' si no existe.

    Esta tabla almacena tanto los datos generales de la persona
    (recogidos en la tabla 'personas') como los específicos de paciente,
    y enlaza mediante claves foráneas con enfermeros, médicos y habitaciones.
    Columnas en orden:
      0 id            TEXT    PK      → clave foránea a personas(id)
      1 username      TEXT    UNIQUE NOT NULL
      2 password      TEXT    NOT NULL
      3 nombre        TEXT    NOT NULL
      4 apellido      TEXT    NOT NULL
      5 edad          INTEGER NOT NULL
      6 genero        TEXT    NOT NULL
      7 estado        TEXT    NOT NULL
      8 historial_medico TEXT  NULL    (JSON)
      9 id_enfermero  TEXT    NULL    FK → enfermeros(id)
     10 id_medico     TEXT    NULL    FK → medicos(id)
     11 id_habitacion TEXT    NULL    FK → habitaciones(numero_habitacion)
     12 rol           TEXT    DEFAULT 'paciente'
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT NOT NULL,
            historial_medico TEXT,
            id_enfermero TEXT,
            id_medico TEXT,
            id_habitacion TEXT,
            rol TEXT DEFAULT 'paciente',
            FOREIGN KEY (id)           REFERENCES personas(id)              ON DELETE CASCADE,
            FOREIGN KEY (id_enfermero) REFERENCES enfermeros(id),
            FOREIGN KEY (id_medico)    REFERENCES medicos(id),
            FOREIGN KEY (id_habitacion)REFERENCES habitaciones(numero_habitacion)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'pacientes' creada correctamente.")


def insertar_paciente(
    id: str,
    username: str,
    password: str,
    nombre: str,
    apellido: str,
    edad: int,
    genero: str,
    estado: str,
    historial_medico: list,
    id_enfermero: str,
    id_medico: str,
    id_habitacion: str
) -> None:
    """
    Inserta un nuevo paciente en la tabla 'pacientes'.

    Parámetros
    ----------
    id : str
        Identificador único (debe existir en 'personas').
    username : str
        Nombre de usuario (único).
    password : str
        Contraseña en texto plano o hash.
    nombre : str
        Nombre de la persona.
    apellido : str
        Apellido de la persona.
    edad : int
        Edad de la persona.
    genero : str
        Género de la persona.
    estado : str
        Estado de salud del paciente.
    historial_medico : list, opcional
        Lista de anotaciones (se convierte a JSON).
    id_enfermero : str, opcional
        ID del enfermero asignado.
    id_medico : str, opcional
        ID del médico asignado.
    id_habitacion : str, opcional
        Número de habitación asignada.
    """
    historial_str = json.dumps(historial_medico) if historial_medico else None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pacientes (
                id, username, password, nombre, apellido,
                edad, genero, estado, historial_medico,
                id_enfermero, id_medico, id_habitacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            id, username, password, nombre, apellido,
            edad, genero, estado, historial_str,
            id_enfermero, id_medico, id_habitacion
        ))
        conn.commit()
        print(f"Paciente con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError as e:
        print("Error de inserción:", e)
    finally:
        conn.close()


def leer_pacientes() -> list[tuple]:
    """
    Recupera todos los registros de la tabla 'pacientes'.

    Devuelve
    --------
    list of tuple
        Cada tupla contiene los 13 campos de la tabla en el orden definido.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def eliminar_paciente(id: str) -> None:
    """
    Elimina un paciente de la base de datos según su ID.

    Parámetros
    ----------
    id : str
        Identificador del paciente a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Paciente '{id}' eliminado correctamente.")


def crear_tabla_paciente_enfermedad() -> None:
    """
    Crea la tabla intermedia 'paciente_enfermedad' para la relación N:N entre pacientes y enfermedades.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paciente_enfermedad (
            id_paciente TEXT NOT NULL,
            id_enfermedad TEXT NOT NULL,
            PRIMARY KEY (id_paciente, id_enfermedad),
            FOREIGN KEY (id_paciente)   REFERENCES pacientes(id),
            FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'paciente_enfermedad' creada correctamente.")


if __name__ == "__main__":
    crear_tabla_pacientes()
    crear_tabla_paciente_enfermedad()
paciente = leer_pacientes()
