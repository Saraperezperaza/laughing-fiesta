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
    # Habilitar claves foráneas
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def crear_tabla_citas():
    """
    Crea la tabla 'citas' en la base de datos si no existe.

    La tabla contiene:
    - id_cita: identificador único de la cita.
    - paciente: nombre o ID del paciente.
    - medico: nombre o ID del médico.
    - motivo: descripción del motivo de la cita.
    - fecha_hora: fecha y hora en formato texto.
    - estado: estado de la cita ('pendiente', 'completado', 'cancelado').
    - atendido: valor booleano (0 o 1) que indica si fue atendida.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id_cita TEXT PRIMARY KEY,
            paciente TEXT NOT NULL,
            medico TEXT NOT NULL,
            motivo TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            atendido INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'citas' creada correctamente.")

def insertar_cita(
    id_cita: str,
    paciente: str,
    medico: str,
    motivo: str,
    fecha_hora: str,
    estado: str = 'pendiente',
    atendido: bool = False
):
    """
    Inserta una nueva cita médica en la base de datos.

    Parámetros
    ----------
    id_cita : str
        Identificador único de la cita.
    paciente : str
        Nombre o identificador del paciente.
    medico : str
        Nombre o identificador del médico.
    motivo : str
        Motivo de la cita.
    fecha_hora : str
        Fecha y hora de la cita (en formato de texto).
    estado : str, opcional
        Estado de la cita (por defecto 'pendiente').
    atendido : bool, opcional
        Indica si la cita ha sido atendida (por defecto False).
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO citas (
            id_cita, paciente, medico, motivo, fecha_hora, estado, atendido
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_cita, paciente, medico, motivo, fecha_hora, estado, int(atendido)))
    conn.commit()
    conn.close()
    print(f"Cita {id_cita} insertada correctamente.")

def leer_citas():
    """
    Recupera todas las citas almacenadas en la base de datos.

    Devuelve
    --------
    Lista
        Lista con las filas de la tabla 'citas'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def actualizar_cita(
    id_cita: str,
    nuevo_estado: str = None,
    atendido: bool = None
):
    """
    Actualiza el estado y/o el campo de atención de una cita existente.

    Parámetros
    ----------
    id_cita : str
        Identificador de la cita a modificar.
    nuevo_estado : str, opcional
        Nuevo estado a asignar a la cita ('pendiente', 'completado', etc.).
    atendido : bool, opcional
        Nuevo valor para indicar si fue atendida.
    """
    conn = conectar()
    cursor = conn.cursor()
    if nuevo_estado:
        cursor.execute("UPDATE citas SET estado = ? WHERE id_cita = ?", (nuevo_estado, id_cita))
    if atendido is not None:
        cursor.execute("UPDATE citas SET atendido = ? WHERE id_cita = ?", (int(atendido), id_cita))
    conn.commit()
    conn.close()
    print(f"Cita {id_cita} actualizada.")

def eliminar_cita(id_cita: str):
    """
    Elimina una cita de la base de datos según su identificador.

    Parámetros
    ----------
    id_cita : str
        Identificador de la cita a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE id_cita = ?", (id_cita,))
    conn.commit()
    conn.close()
    print(f"Cita {id_cita} eliminada.")

if __name__ == "__main__":
    crear_tabla_citas()
