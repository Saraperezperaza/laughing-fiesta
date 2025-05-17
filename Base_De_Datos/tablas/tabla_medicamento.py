import sqlite3
from datetime import datetime

def conectar():
    """
    Establece la conexión con la base de datos SQLite.

    Devuelve
    --------
    sqlite3.Connection
        Objeto de conexión a la base de datos '../base_de_datos.db'.
    """
    return sqlite3.connect('../base_de_datos.db')


def crear_tabla_medicamentos() -> None:
    """
    Crea la tabla 'medicamentos' si no existe en la base de datos.

    La tabla incluye los siguientes campos:
    - id: identificador único del medicamento.
    - nombre: nombre del medicamento.
    - dosis: dosis recomendada.
    - precio: precio del medicamento.
    - fecha_caducidad: fecha en la que expira el medicamento.
    - alergenos: lista de posibles alérgenos (como texto separado por comas).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicamentos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            dosis TEXT NOT NULL,
            precio REAL NOT NULL,
            fecha_caducidad TEXT NOT NULL,
            alergenos TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'medicamentos' creada correctamente.")


def insertar_medicamento(
    id: str,
    nombre: str,
    dosis: str,
    precio: float,
    fecha_caducidad: datetime | str,
    alergenos: list | None = None
) -> None:
    """
    Inserta un medicamento en la base de datos.

    Parámetros
    ----------
    id : str
        Identificador único del medicamento.
    nombre : str
        Nombre del medicamento.
    dosis : str
        Dosis recomendada.
    precio : float
        Precio del medicamento.
    fecha_caducidad : datetime o str
        Fecha de caducidad del medicamento (se convierte a 'YYYY-MM-DD').
    alergenos : list de str, opcional
        Lista de alérgenos separados por comas.
    """
    if isinstance(fecha_caducidad, datetime):
        fecha_caducidad = fecha_caducidad.strftime('%Y-%m-%d')
    alergenos_str = ','.join(alergenos) if alergenos else None

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medicamentos (
                id, nombre, dosis, precio, fecha_caducidad, alergenos
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, nombre, dosis, precio, fecha_caducidad, alergenos_str))
        conn.commit()
        print(f"Medicamento '{nombre}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: ID de medicamento ya existe.")
    finally:
        conn.close()


def leer_medicamentos() -> list:
    """
    Recupera todos los medicamentos registrados en la base de datos.

    Devuelve
    --------
    Lista
        Lista de tuplas con los medicamentos existentes.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicamentos")
    medicamentos = cursor.fetchall()
    conn.close()
    return medicamentos


def eliminar_medicamento(id: str) -> None:
    """
    Elimina un medicamento dado su ID.

    Parámetros
    ----------
    id : str
        Identificador del medicamento a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicamentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Medicamento {id} eliminado.")


def crear_tabla_medicamento_enfermedad() -> None:
    """
    Crea la tabla intermedia 'medicamento_enfermedad' para establecer una relación N:N
    entre medicamentos y enfermedades.

    La tabla contiene:
    - id_medicamento: clave foránea al campo id de medicamentos.
    - id_enfermedad: clave foránea al campo id de enfermedades.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicamento_enfermedad (
            id_medicamento TEXT NOT NULL,
            id_enfermedad TEXT NOT NULL,
            PRIMARY KEY (id_medicamento, id_enfermedad),
            FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id),
            FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'medicamento_enfermedad' creada correctamente.")


if __name__ == "__main__":
    crear_tabla_medicamentos()
    crear_tabla_medicamento_enfermedad()
