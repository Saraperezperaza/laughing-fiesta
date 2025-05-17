import sqlite3

def conectar() -> sqlite3.Connection:
    """
    Establece la conexión con la base de datos SQLite.

    Devuelve
    -------
    sqlite3.Connection
        Objeto de conexión a la base de datos 'base_de_datos.db'.
    """
    return sqlite3.connect('../base_de_datos.db')

def crear_tabla_ambulancias() -> None:
    """
    Crea la tabla 'ambulancias' en la base de datos si no existe.

    La tabla contiene los siguientes campos:
    - matricula (clave primaria)
    - zona
    - modelo
    - sirena ('bitonal' o 'secuencial')
    - id_centro (clave foránea referida a la tabla 'centros')
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ambulancias (
            matricula TEXT PRIMARY KEY,
            zona TEXT NOT NULL,
            modelo TEXT NOT NULL,
            sirena TEXT NOT NULL CHECK (sirena IN ('bitonal', 'secuencial')),
            id_centro TEXT NOT NULL,
            FOREIGN KEY (id_centro) REFERENCES centros(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabla 'ambulancias' creada correctamente.")

def insertar_ambulancia(matricula: str, zona: str, modelo: str, sirena: str, id_centro: str) -> None:
    """
    Inserta una nueva ambulancia en la base de datos.

    Parametros
    ----------
    matricula : str
        Matrícula única de la ambulancia.
    zona : str
        Zona asignada a la ambulancia.
    modelo : str
        Modelo del vehículo.
    sirena : str
        Tipo de sirena ('bitonal' o 'secuencial').
    id_centro : str
        Identificador del centro al que pertenece la ambulancia.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ambulancias (matricula, zona, modelo, sirena, id_centro)
            VALUES (?, ?, ?, ?, ?)
        ''', (matricula, zona, modelo, sirena, id_centro))
        conn.commit()
        print("Ambulancia insertada con éxito.")
    except sqlite3.IntegrityError as e:
        print("Error de integridad:", e)
    except Exception as e:
        print("Error al insertar ambulancia:", e)
    finally:
        conn.close()

def leer_ambulancias() -> list:
    """
    Recupera todos los registros de ambulancias almacenados.

    Devuelve
    -------
    Lista
        Lista de tuplas, cada una representando una ambulancia.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ambulancias")
    ambulancias = cursor.fetchall()
    conn.close()
    return ambulancias

def actualizar_ambulancia(
    matricula: str,
    nueva_zona: str = None,
    nuevo_modelo: str = None,
    nueva_sirena: str = None,
    nuevo_id_centro: str = None
) -> None:
    """
    Actualiza los datos de una ambulancia existente.

    Parametros
    ----------
    matricula : str
        Matrícula de la ambulancia a actualizar.
    nueva_zona : str, optional
        Nueva zona asignada.
    nuevo_modelo : str, optional
        Nuevo modelo del vehículo.
    nueva_sirena : str, optional
        Nuevo tipo de sirena.
    nuevo_id_centro : str, optional
        Nuevo ID del centro al que se asocia la ambulancia.
    """
    conn = conectar()
    cursor = conn.cursor()
    if nueva_zona:
        cursor.execute("UPDATE ambulancias SET zona = ? WHERE matricula = ?", (nueva_zona, matricula))
    if nuevo_modelo:
        cursor.execute("UPDATE ambulancias SET modelo = ? WHERE matricula = ?", (nuevo_modelo, matricula))
    if nueva_sirena:
        cursor.execute("UPDATE ambulancias SET sirena = ? WHERE matricula = ?", (nueva_sirena, matricula))
    if nuevo_id_centro:
        cursor.execute("UPDATE ambulancias SET id_centro = ? WHERE matricula = ?", (nuevo_id_centro, matricula))
    conn.commit()
    conn.close()
    print(f"Ambulancia {matricula} actualizada.")

def eliminar_ambulancia(matricula: str) -> None:
    """
    Elimina una ambulancia de la base de datos por su matrícula.

    Parametros
    ----------
    matricula : str
        Matrícula de la ambulancia a eliminar.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ambulancias WHERE matricula = ?", (matricula,))
    conn.commit()
    conn.close()
    print(f"Ambulancia {matricula} eliminada.")

if __name__ == "__main__":
    crear_tabla_ambulancias()

