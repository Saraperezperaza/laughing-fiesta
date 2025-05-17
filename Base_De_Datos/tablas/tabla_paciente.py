import sqlite3
import json

def conectar() -> sqlite3.Connection:
    """
    Establece una conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Conexión activa a la base de datos.
    """
    return sqlite3.connect('../base_de_datos.db')


def crear_tabla_pacientes() -> None:
    """
    Crea la tabla 'pacientes' con herencia real desde la tabla 'personas'.

    Esta tabla contiene datos específicos de pacientes y se enlaza
    con la tabla 'personas' mediante la clave foránea 'id'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id TEXT PRIMARY KEY,
            estado TEXT NOT NULL,
            historial_medico TEXT,
            id_enfermero TEXT,
            id_medico TEXT,
            id_habitacion TEXT,
            FOREIGN KEY (id) REFERENCES personas(id) ON DELETE CASCADE,
            FOREIGN KEY (id_enfermero) REFERENCES enfermeros(id),
            FOREIGN KEY (id_medico) REFERENCES medicos(id),
            FOREIGN KEY (id_habitacion) REFERENCES habitaciones(numero_habitacion)
        )
    ''')

    conn.commit()
    conn.close()
    print("Tabla 'pacientes' creada correctamente.")


def insertar_paciente(
    id: str,
    estado: str,
    historial_medico: list | None = None,
    id_enfermero: str = None,
    id_medico: str = None,
    id_habitacion: str = None
) -> None:
    """
    Inserta un nuevo paciente en la tabla 'pacientes'.

    Requiere que la persona ya haya sido registrada en la tabla 'personas'.

    Parámetros
    ----------
    id : str
        Identificador único del paciente (ya debe existir en 'personas').
    estado : str
        Estado de salud del paciente.
    historial_medico : list, opcional
        Historial médico en formato lista (se convierte a JSON).
    id_enfermero : str, opcional
        ID del enfermero asignado.
    id_medico : str, opcional
        ID del médico asignado.
    id_habitacion : str, opcional
        ID de la habitación asignada.
    """
    historial_str = json.dumps(historial_medico) if historial_medico else None

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pacientes (
                id, estado, historial_medico, id_enfermero, id_medico, id_habitacion
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, estado, historial_str, id_enfermero, id_medico, id_habitacion))
        conn.commit()
        print(f"Paciente con ID '{id}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: ID no existe en personas o ya fue registrado como paciente.")
    finally:
        conn.close()


def leer_pacientes() -> list[tuple]:
    """
    Recupera todos los registros de la tabla 'pacientes'.

    Devuelve
    --------
    list of tuple
        Tuplas con los datos específicos de cada paciente.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes


def eliminar_paciente(id: str) -> None:
    """
    Elimina un paciente de la base de datos.

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
    print(f"Paciente {id} eliminado.")


def crear_tabla_paciente_enfermedad() -> None:
    """
    Crea la tabla intermedia 'paciente_enfermedad' para relación N:N entre pacientes y enfermedades.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paciente_enfermedad (
            id_paciente TEXT NOT NULL,
            id_enfermedad TEXT NOT NULL,
            PRIMARY KEY (id_paciente, id_enfermedad),
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
            FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'paciente_enfermedad' creada correctamente.")


if __name__ == "__main__":
    crear_tabla_pacientes()
    crear_tabla_paciente_enfermedad()
