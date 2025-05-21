"""
API Salud
==========

Módulo principal de la API Flask para el sistema de gestión hospitalaria.
Ofrece:
  - Gestión de SIPS (Sistema de Identificación de Pacientes)
  - CRUD de Pacientes, Médicos, Enfermeros, Auxiliares, Habitaciones
  - Asignaciones Paciente→Médico y Paciente→Habitación
  - Consulta de información de medicamentos via RxNorm
  - Generación de PDF con datos de paciente

Persistencia mediante SQLite, usando módulos en Base_De_Datos/tablas.
"""
from flask import Flask, request, jsonify
from functools import wraps
import requests
import uuid
import sqlite3
import os

# Importar módulos de BD
from Base_De_Datos.tablas.tabla_SIPS import crear_tabla_sip, insertar_sip, leer_sip, eliminar_sip
from Base_De_Datos.tablas.tabla_paciente import crear_tabla_pacientes, insertar_paciente, leer_pacientes, eliminar_paciente
from Base_De_Datos.tablas.tabla_medico import crear_tabla_medicos, insertar_medico, leer_medicos, eliminar_medico
from Base_De_Datos.tablas.tabla_enfermero import crear_tabla_enfermeros, insertar_enfermero, leer_enfermeros, eliminar_enfermero
from Base_De_Datos.tablas.tabla_habitacion import crear_tabla_habitaciones, insertar_habitacion, leer_habitaciones, limpiar_habitacion, eliminar_habitacion
from Base_De_Datos.tablas.tabla_auxiliar import crear_tabla_auxiliares, insertar_auxiliar, leer_auxiliares, eliminar_auxiliar

# Importar utilidades externas
from generador_pdf import generar_pdf_paciente

# Configuración RxNorm
RXNORM_URL = "https://rxnav.nlm.nih.gov/REST/drugs.json"

# Inicializar Flask
app = Flask(__name__)

# Crear tablas al inicio
crear_tabla_sip()
crear_tabla_pacientes()
crear_tabla_medicos()
crear_tabla_enfermeros()
crear_tabla_habitaciones()
crear_tabla_auxiliares()

# Helper para conexiones directas (para actualizaciones sencillas)
def _conectar_bd():
    """
    Conecta a la base de datos SQLite con claves foráneas habilitadas.

    Returns
        -------
        sqlite3.Connection
            Objeto de conexión SQLite.
    """
    path = os.path.join(os.path.dirname(__file__), 'Base_De_Datos', 'tablas', 'bdd.db')
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Autenticación
def requiere_autenticacion(f):
    """
        Decorador de autenticación HTTP básica con rol en cabecera 'X-ROL'.

        Parameters
        ----------
        f : Callable
            Vista de Flask a proteger.

        Returns
        -------
        Callable
            Función decorada que recibe usuario autenticado.
        """
    @wraps(f)
    def deco(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({"detail": "Autenticación requerida."}), 401
        # Extraer rol del header
        rol = request.headers.get('X-ROL')
        user = auth.username
        pwd  = auth.password
        # Validar según rol consultando BD
        if rol == 'paciente':
            filas = leer_pacientes()
            users = {r[1]: r for r in filas}  # username->row
        elif rol == 'medico':
            filas = leer_medicos()
            users = {r[1]: r for r in filas}
        elif rol == 'enfermero':
            filas = leer_enfermeros()
            users = {r[1]: r for r in filas}
        else:
            return jsonify({"detail": "Rol no reconocido."}), 403
        registro = users.get(user)
        if not registro or registro[2] != pwd:
            return jsonify({"detail": "Credenciales inválidas."}), 401
        # Usuario autenticado
        class U: pass
        usuario = U()
        usuario.id = registro[0]
        usuario.rol = rol
        return f(usuario, *args, **kwargs)
    return deco

# === Endpoints básicos ===
@app.route('/')
def home():
    """
    Verifica que la API está en línea.

    Returns
    -------
    Response
        Mensaje de estado.
    """
    return jsonify({"mensaje": "API Salud funcionando."})

@app.route('/test')
def test():
    """
    Endpoint de prueba.

    Returns
    -------
    Response
        Mensaje de confirmación.
    """
    return jsonify({"mensaje": "Test OK."})

# RxNorm
@app.route('/medicamento/info', methods=['GET'])
def info_medicamento():
    """
    Consulta la API RxNorm para un medicamento.

    Returns
    -------
    Response
        JSON con datos o error.
    """
    nombre = request.args.get('name')
    if not nombre:
        return jsonify({"error": "Parámetro 'name' requerido."}), 400
    try:
        resp = requests.get(RXNORM_URL, params={'name': nombre})
        resp.raise_for_status()
        data = resp.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 502

# Menú por rol
@app.route('/menu', methods=['GET'])
@requiere_autenticacion
def menu(usuario):
    """
    Devuelve opciones de menú según rol.
    Returns
    -------
    Response
        JSON con lista de opciones.
    """
    if usuario.rol == 'paciente':
        opciones = ["Ver info", "Pedir cita", "Descargar PDF", "Recomendar medicamento"]
    elif usuario.rol == 'medico':
        opciones = ["Listar pacientes", "Ver citas", "Historial médico"]
    elif usuario.rol == 'enfermero':
        opciones = ["Ver habitaciones", "Asignar paciente", "Limpiar habitación"]
    else:
        opciones = []
    return jsonify({"rol": usuario.rol, "menu": opciones})

# SIPS
@app.route('/crear_sip/<paciente_id>', methods=['GET'])
def crear_sip(paciente_id):
    """
    Genera y almacena un SIP para un paciente.

    Parameters
    ----------
    paciente_id : str
        ID del paciente.

    Returns
    -------
    Response
        JSON con SIP o error.
    """
    if leer_sip(paciente_id):
        return jsonify({"error": "SIP ya existe."}), 400
    sip = f"SIP-{uuid.uuid4().hex[:10].upper()}"
    insertar_sip(sip, paciente_id)
    return jsonify({"sip": sip}), 201

@app.route('/consultar_sip/<paciente_id>', methods=['GET'])
def consultar_sip(paciente_id):
    """
    Recupera el SIP de un paciente.

    Parameters
    ----------
    paciente_id : str
        ID del paciente.

    Returns
    -------
    Response
        JSON con SIP o 404.
    """
    sip = leer_sip(paciente_id)
    if not sip:
        return jsonify({"error": "No existe SIP."}), 404
    return jsonify({"sip": sip})

@app.route('/eliminar_sip/<paciente_id>', methods=['DELETE'])
def eliminar_sip_endpoint(paciente_id):
    """
    Elimina el SIP de un paciente.

    Parameters
    ----------
    paciente_id : str
        ID del paciente.

    Returns
    -------
    Response
        Mensaje de confirmación.
    """
    if not leer_sip(paciente_id):
        return jsonify({"error": "No existe SIP."}), 404
    eliminar_sip(paciente_id)
    return jsonify({"mensaje": "SIP eliminado."})

# === Pacientes CRUD ===
@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    """
    Lista todos los pacientes.

    Returns
    -------
    Response
        JSON con detalles de pacientes.
    """
    filas = leer_pacientes()
    res = []
    for (id_, user, pwd, nom, ape, edad, gen, est, hist, id_enf, id_med, id_hab, rol) in filas:
        res.append({"id":id_, "username":user, "nombre":nom, "apellido":ape,
                    "edad":edad, "genero":gen, "estado":est,
                    "id_enfermero":id_enf, "id_medico":id_med, "id_habitacion":id_hab})
    return jsonify(res)
@app.route('/pacientes/alta', methods=['POST'])
def alta_paciente():
    """
    Da de alta un nuevo paciente.

    Parameters
    ----------
    JSON body con campos obligatorios y opcionales:
      - id, username, password, nombre, apellido, edad, genero, estado
      - historial_medico?, id_enfermero?, id_medico?, id_habitacion?

    Returns
    -------
    Response
        Estado 201 o mensaje de error.
    """
    d = request.json
    try:
        insertar_paciente(
            paciente_id = d['id'],
            username = d['username'],
            password = d['password'],
            nombre = d['nombre'],
            apellido = d['apellido'],
            edad = d['edad'],
            genero = d['genero'],
            estado = d['estado'],
            historial_medico = d.get('historial_medico'),
            id_enfermero = d.get('id_enfermero'),
            id_medico = d.get('id_medico'),
            id_habitacion = d.get('id_habitacion')
        )
        return jsonify({"mensaje":"Paciente dado de alta."}), 201
    except ValueError as e:
        return jsonify({"error":str(e)}), 400

@app.route('/pacientes/baja/<paciente_id>', methods=['DELETE'])
def baja_paciente(paciente_id:str):
    """
    Elimina un paciente.

    Parameters
    ----------
    paciente_id : str
        ID del paciente.

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    ids = {r[0] for r in leer_pacientes()}
    if paciente_id not in ids:
        return jsonify({"error":"Paciente no existe."}), 404
    eliminar_paciente(paciente_id)
    return jsonify({"mensaje":"Paciente eliminado."})

# === Médicos CRUD ===
@app.route('/medicos', methods=['GET'])
def listar_medicos():
    """
    Lista todos los médicos.

    Returns
    -------
    Response
        JSON con detalles de médicos.
    """
    return jsonify([
        {"id":m[0], "username":m[1], "especialidad":m[3], "antiguedad":m[4]}
        for m in leer_medicos()
    ])

@app.route('/medicos/alta', methods=['POST'])
def alta_medico():
    """
    Registra un nuevo médico.

    Parameters
    ----------
    JSON body:
      - id, username, password, especialidad, antiguedad

    Returns
    -------
    Response
        Estado 201 o mensaje de error.
    """
    d = request.json
    # Validar campos obligatorios
    if 'especialidad' not in d or 'antiguedad' not in d:
        return jsonify({"error": "Debe indicar 'especialidad' y 'antiguedad'."}), 400
    try:
        insertar_medico(
            medico_id    = d['id'],
            username     = d['username'],
            password     = d['password'],
            especialidad = d['especialidad'],
            antiguedad   = int(d['antiguedad'])
        )
        return jsonify({"mensaje":"Médico dado de alta."}), 201
    except ValueError as e:
        return jsonify({"error":str(e)}), 400

@app.route('/medicos/baja/<medico_id>', methods=['DELETE'])
def baja_medico(medico_id):
    """
    Elimina un médico.

    Parameters
    ----------
    medico_id : str
        ID del médico.

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    ids = {r[0] for r in leer_medicos()}
    if medico_id not in ids:
        return jsonify({"error":"Médico no existe."}), 404
    eliminar_medico(medico_id)
    return jsonify({"mensaje":"Médico eliminado."})

# === Enfermeros CRUD ===
@app.route('/enfermeros', methods=['GET'])
def listar_enfermeros():
    """
    Lista todos los enfermeros.

    Returns
    -------
    Response
        JSON con detalles de enfermeros.
    """
    return jsonify([
        {"id": e[0], "username": e[1]}
        for e in leer_enfermeros()
    ])

@app.route('/enfermeros/alta', methods=['POST'])
def alta_enfermero():
    """
    Registra un nuevo enfermero.

    Parameters
    ----------
    JSON body:
      - id, username, password

    Returns
    -------
    Response
        Estado 201 o mensaje de error.
    """
    d = request.json
    # Validar campos obligatorios
    if 'username' not in d or 'password' not in d:
        return jsonify({"error": "Debe indicar 'username' y 'password'."}), 400
    try:
        insertar_enfermero(
            enfermero_id = d['id'],
            username     = d['username'],
            password     = d['password'],
            antiguedad =  (d['antieguedad']),
            especialidad = d['especialidad']
        )
        return jsonify({"mensaje": "Enfermero dado de alta."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/enfermeros/baja/<enf_id>', methods=['DELETE'])
def baja_enfermero(enf_id):
    """
    Elimina un enfermero.

    Parameters
    ----------
    enf_id : str
        ID del enfermero.

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    # Comprobar existencia del enfermero
    ids = {r[0] for r in leer_enfermeros()}
    if enf_id not in ids:
        return jsonify({"error": "Enfermero no existe."}), 404
    eliminar_enfermero(enf_id)
    return jsonify({"mensaje": "Enfermero eliminado."})

# === Auxiliares CRUD ===
@app.route('/auxiliares', methods=['GET'])
def listar_auxiliares():
    """
    Lista todos los auxiliares.

    Returns
    -------
    Response
        JSON con detalles de auxiliares.
    """
    return jsonify([
        {"id":a[0], "antiguedad":a[1], "id_enfermero":a[2]}
        for a in leer_auxiliares()
    ])

@app.route('/auxiliares/alta', methods=['POST'])
def alta_auxiliar():
    """
    Registra un nuevo auxiliar.

    Parameters
    ----------
    JSON body:
      - id, antiguedad, id_enfermero?

    Returns
    -------
    Response
        Estado 201 o mensaje de error.
    """
    d = request.json
    try:
        insertar_auxiliar(
            id           = d['id'],
            antiguedad   = d['antiguedad'],
            id_enfermero = d.get('id_enfermero')
        )
        return jsonify({"mensaje":"Auxiliar dado de alta."}), 201
    except ValueError as e:
        return jsonify({"error":str(e)}), 400

@app.route('/auxiliares/baja/<aux_id>', methods=['DELETE'])
def baja_auxiliar(aux_id):
    """
    Elimina un auxiliar.

    Parameters
    ----------
    aux_id : str
        ID del auxiliar.

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    ids = {r[0] for r in leer_auxiliares()}
    if aux_id not in ids:
        return jsonify({"error":"Auxiliar no existe."}), 404
    eliminar_auxiliar(aux_id)
    return jsonify({"mensaje":"Auxiliar eliminado."})

# === Habitaciones CRUD ===
@app.route('/habitaciones', methods=['GET'])
def listar_habitaciones():
    """
    Lista todas las habitaciones.

    Returns
    -------
    Response
        JSON con detalles de habitaciones.
    """
    return jsonify([
        {"numero":h[0], "capacidad":h[1], "limpia":bool(h[2])}
        for h in leer_habitaciones()
    ])

@app.route('/habitaciones/alta', methods=['POST'])
def alta_habitacion():
    """
    Registra una nueva habitación.

    Parameters
    ----------
    JSON body:
      - numero, capacidad

    Returns
    -------
    Response
        Estado 201 o mensaje de error.
    """
    d = request.json
    try:
        insertar_habitacion(
            numero_habitacion = d['numero'],
            capacidad         = d['capacidad']
        )
        return jsonify({"mensaje":"Habitación dada de alta."}), 201
    except ValueError as e:
        return jsonify({"error":str(e)}), 400

@app.route('/habitaciones/limpiar/<int:numero>', methods=['PATCH'])
def habitacion_limpiar(numero):
    """
    Marca una habitación como limpia.

    Parameters
    ----------
    numero : int
        Número de habitación.

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    nums = {r[0] for r in leer_habitaciones()}
    if numero not in nums:
        return jsonify({"error":"Habitación no existe."}), 404
    limpiar_habitacion(numero)
    return jsonify({"mensaje":"Habitación limpiada."})

@app.route('/habitaciones/baja/<int:numero>', methods=['DELETE'])
def baja_habitacion(numero):
    """
    Elimina una habitación.

    Parameters
    ----------
    numero : int
        Número de habitación.

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    nums = {r[0] for r in leer_habitaciones()}
    if numero not in nums:
        return jsonify({"error":"Habitación no existe."}), 404
    eliminar_habitacion(numero)
    return jsonify({"mensaje":"Habitación eliminada."})

# === Asignaciones 1:N ===
@app.route('/pacientes/asignar_medico', methods=['POST'])
def asignar_medico():
    """
    Asigna un médico a un paciente.

    Parameters
    ----------
    JSON body:
      - id_paciente : str
      - id_medico   : str

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    d = request.json
    id_p = d['id_paciente']; id_m = d['id_medico']
    pacientes_ids = {r[0] for r in leer_pacientes()}
    medicos_ids   = {r[0] for r in leer_medicos()}
    if id_p not in pacientes_ids or id_m not in medicos_ids:
        return jsonify({"error":"Paciente o médico no existe."}), 404
    conn = _conectar_bd()
    conn.execute("UPDATE pacientes SET id_medico=? WHERE id=?;", (id_m, id_p))
    conn.commit(); conn.close()
    return jsonify({"mensaje":"Médico asignado."})

@app.route('/pacientes/asignar_habitacion', methods=['POST'])

def asignar_habitacion():
    """
    Asigna una habitación a un paciente.

    Parameters
    ----------
    JSON body:
      - id_paciente : str
      - numero      : int

    Returns
    -------
    Response
        Mensaje de confirmación o error.
    """
    d = request.json
    id_p = d['id_paciente']; num = d['numero']
    pacientes_ids = {r[0] for r in leer_pacientes()}
    hab_ids       = {r[0] for r in leer_habitaciones()}
    if id_p not in pacientes_ids or num not in hab_ids:
        return jsonify({"error":"Paciente o habitación no existe."}), 404
    conn = _conectar_bd()
    conn.execute("UPDATE pacientes SET id_habitacion=? WHERE id=?;", (num, id_p))
    conn.commit(); conn.close()
    return jsonify({"mensaje":"Habitación asignada."})

# === Descargar PDF ===
@app.route('/paciente/descargar_pdf', methods=['GET'])
@requiere_autenticacion
def descargar_pdf(usuario):
    """
    Genera un PDF con la información del paciente autenticado.

    Parameters
    ----------
    usuario/rol: object
        Usuario autenticado con rol 'paciente'.

    Returns
    -------
    Response
        JSON con nombre de archivo PDF o error.
    """
    if usuario.rol != 'paciente':
        return jsonify({"error":"Acceso denegado."}), 403
    paciente_id = usuario.id
    filas = [r for r in leer_pacientes() if r[0] == paciente_id]
    if not filas:
        return jsonify({"error": "Paciente no existe."}), 404
    paciente_id = usuario.id
    filas = [r for r in leer_pacientes() if r[0] == paciente_id]
    if not filas:
        return jsonify({"error": "Paciente no existe."}), 404
    # Convertir la tupla en un diccionario para el generador de PDF
    campos = ['id', 'username', 'password', 'nombre', 'apellido', 'edad',
              'genero', 'estado', 'historial_medico', 'id_enfermero',
              'id_medico', 'id_habitacion', 'rol']
    datos = filas[0]
    paciente_dict = dict(zip(campos, datos))
    try:
        nombre_pdf = generar_pdf_paciente(paciente_dict) # type: ignore[arg-type]
        return jsonify({"pdf": nombre_pdf})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
