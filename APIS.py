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
import logging
from flask import Flask, request, jsonify
from functools import wraps
import requests
import uuid
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash  # Importar para hashing
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
from sqlalchemy import Column, Integer, String

# Importar módulos de BD
from Base_De_Datos.tablas.tabla_SIPS import crear_tabla_sip, insertar_sip, leer_sip, eliminar_sip
from Base_De_Datos.tablas.tabla_paciente import crear_tabla_pacientes, insertar_paciente, leer_pacientes, eliminar_paciente
from Base_De_Datos.tablas.tabla_medico import crear_tabla_medicos, insertar_medico, leer_medicos, eliminar_medico
from Base_De_Datos.tablas.tabla_enfermero import crear_tabla_enfermeros, insertar_enfermero, leer_enfermeros, eliminar_enfermero
from Base_De_Datos.tablas.tabla_habitacion import crear_tabla_habitaciones, insertar_habitacion, leer_habitaciones, limpiar_habitacion, eliminar_habitacion
from Base_De_Datos.tablas.tabla_auxiliar import crear_tabla_auxiliares, insertar_auxiliar, leer_auxiliares, eliminar_auxiliar

# Importar utilidades externas
from generador_pdf import generar_pdf_paciente
import gestor_de_citas
from gestor_de_citas import CitaPresencial, CitaTelefonica, CitaUrgencias, GestorCitas
from Base_De_Datos.tablas.modelos import PacienteDB, MedicoDB, EnfermeroDB  # Importación corregida
from Clases_Base_de_datos.paciente import Paciente
# Configuración RxNorm
RXNORM_URL = "https://rxnav.nlm.nih.gov/REST/drugs.json"

# Inicializar Flask
app = Flask(__name__)
# --- Configuración de la base de datos ---
DATABASE_URL = "sqlite:///./Base_De_Datos/tablas/bdd.db"
engine = create_engine(DATABASE_URL, echo=False)  # echo=True para ver las consultas SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Crear tablas al inicio (Comentado para usar SQLAlchemy si los modelos están definidos)
# crear_tabla_sip()
# crear_tabla_pacientes()
# crear_tabla_medicos()
# crear_tabla_enfermeros()
# crear_tabla_habitaciones()
# crear_tabla_auxiliares()

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
    @wraps(f)
    def deco(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({"detail": "Autenticación requerida."}), 401
        rol = request.headers.get('X-ROL')
        user = auth.username
        pwd = auth.password
        db = next(get_db())
        registro = None
        if rol == 'paciente':
            registro = db.query(PacienteDB).filter(PacienteDB.username == user).first()
        elif rol == 'medico':
            registro = db.query(MedicoDB).filter(MedicoDB.username == user).first()
        elif rol == 'enfermero':
            registro = db.query(EnfermeroDB).filter(EnfermeroDB.username == user).first()
        else:
            return jsonify({"detail": "Rol no reconocido."}), 403

        if not registro or not check_password_hash(registro.password, pwd):
            return jsonify({"detail": "Credenciales inválidas."}), 401

        class U:
            pass
        usuario = U()
        usuario.id = registro.id
        usuario.rol = rol
        return f(usuario, *args, **kwargs)
    return deco

# === Endpoints básicos ===
@app.route('/')
def home():
    return jsonify({"mensaje": "API Salud funcionando."})

@app.route('/test')
def test():
    return jsonify({"mensaje": "Test OK."})

# RxNorm
@app.route('/medicamento/info', methods=['GET'])
def info_medicamento():
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
    opciones = []
    if usuario.rol == 'paciente':
        opciones = ["Pedir cita", "Descargar PDF de mi informe", "Buscar información de medicamento por nombre", "Ver información de mi SIP"]
    elif usuario.rol == 'medico':
        opciones = ["Listar pacientes", "Listar médicos", "Listar enfermeros", "Listar auxiliares", "Dar de alta paciente", "Dar de baja paciente", "Dar de alta médico", "Dar de baja médico", "Dar de alta enfermero", "Dar de baja enfermero", "Dar de alta auxiliar", "Dar de baja auxiliar", "Asignar médico a paciente", "Asignar habitación a paciente", "Crear SIP para paciente", "Consultar SIP de paciente", "Eliminar SIP de paciente"]
    elif usuario.rol == 'enfermero':
        opciones = ["Listar pacientes", "Listar enfermeros", "Listar habitaciones", "Listar auxiliares", "Dar de alta enfermero", "Dar de baja enfermero", "Dar de alta auxiliar", "Dar de baja auxiliar", "Dar de alta habitación", "Dar de baja habitación", "Limpiar habitación"]
    return jsonify({"rol": usuario.rol, "menu": opciones})

# SIPS
@app.route('/crear_sip/<paciente_id>', methods=['GET'])
def crear_sip(paciente_id):
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT sip FROM sips WHERE paciente_id=?", (paciente_id,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "SIP ya existe."}), 400
    sip = f"SIP-{uuid.uuid4().hex[:10].upper()}"
    cursor.execute("INSERT INTO sips (sip, paciente_id) VALUES (?, ?)", (sip, paciente_id))
    conn.commit()
    conn.close()
    return jsonify({"sip": sip}), 201

@app.route('/consultar_sip/<paciente_id>', methods=['GET'])
def consultar_sip(paciente_id):
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT sip FROM sips WHERE paciente_id=?", (paciente_id,))
    resultado = cursor.fetchone()
    conn.close()
    if not resultado:
        return jsonify({"error": "No existe SIP."}), 404
    return jsonify({"sip": resultado[0]})

@app.route('/eliminar_sip/<paciente_id>', methods=['DELETE'])
def eliminar_sip_endpoint(paciente_id):
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT sip FROM sips WHERE paciente_id=?", (paciente_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "No existe SIP."}), 404
    cursor.execute("DELETE FROM sips WHERE paciente_id=?", (paciente_id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "SIP eliminado."})

# === Pacientes CRUD ===
@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    db = next(get_db())
    pacientes = db.query(PacienteDB).all()
    res = [{"id": p.id, "username": p.username, "nombre": p.nombre, "apellido": p.apellido,
            "edad": p.edad, "genero": p.genero, "estado": p.estado,
            "id_enfermero": p.id_enfermero, "id_medico": p.id_medico, "id_habitacion": p.id_habitacion} for p in pacientes]
    return jsonify(res)

@app.route('/pacientes/alta', methods=['POST'])
def alta_paciente():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos."}), 400
    try:
        hashed_password = generate_password_hash(data['password'])
        nuevo_paciente = PacienteDB(
            id=data['id'], username=data['username'], password=hashed_password,
            nombre=data.get('nombre'), apellido=data.get('apellido'), edad=data.get('edad'),
            genero=data.get('genero'), estado=data.get('estado'),
            historial_medico=data.get('historial_medico'), id_enfermero=data.get('id_enfermero'),
            id_medico=data.get('id_medico'), id_habitacion=data.get('id_habitacion')
        )
        db = next(get_db())
        db.add(nuevo_paciente)
        db.commit()
        return jsonify({"mensaje": "Paciente dado de alta."}), 201
    except KeyError as e:
        db = next(get_db())
        db.rollback()
        return jsonify({"error": f"Campo requerido faltante: {str(e)}"}), 400
    except Exception as e:
        db = next(get_db())
        db.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/pacientes/baja/<paciente_id>', methods=['DELETE'])
def baja_paciente(paciente_id: str):
    db = next(get_db())
    paciente = db.query(PacienteDB).filter(PacienteDB.id == paciente_id).first()
    if not paciente:
        return jsonify({"error": "Paciente no existe."}), 404
    db.delete(paciente)
    db.commit()
    return jsonify({"mensaje": "Paciente eliminado."})

@app.route("/cita/pedir", methods=["POST"])
@requiere_autenticacion
def pedir_cita(usuario):
    data = request.get_json()
    if not data:
        return jsonify({"detail": "No se proporcionaron datos en la solicitud."}), 400
    tipo_cita = data.get("tipo_cita")
    fecha_hora_str = data.get("fecha_hora")
    medico_asignado = data.get("medico", "Sin asignar")
    motivo = data.get("motivo", "")
    username_paciente_id = usuario.id # Este es el ID del paciente

    if not tipo_cita or not fecha_hora_str:
        return jsonify({"detail": "Debes especificar el tipo de cita y la fecha/hora."}), 400

    try:
        fecha_hora_dt = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M:%S')
        fecha_hora_fmt_gestor = fecha_hora_dt.strftime('%Y %m %d %H:%M')
    except ValueError as e:
        return jsonify({"detail": f"Formato de fecha/hora inválido. Usa YYYY-MM-DDTHH:MM:SS: {str(e)}"}), 400

    db = next(get_db())
    try:
        paciente_db_obj = db.query(PacienteDB).filter(PacienteDB.id == username_paciente_id).first()
        if not paciente_db_obj:
            return jsonify({"detail": f"Paciente con ID {username_paciente_id} no encontrado en la base de datos."}), 404

        paciente_obj = Paciente(
            id=paciente_db_obj.id,
            username=paciente_db_obj.username,
            password=paciente_db_obj.password, # Esto es el hash, tu clase Paciente lo acepta
            nombre=paciente_db_obj.nombre,
            apellido=paciente_db_obj.apellido,
            edad=paciente_db_obj.edad,
            genero=paciente_db_obj.genero,
            estado=paciente_db_obj.estado,
            historial_medico=getattr(paciente_db_obj, 'historial_medico', None) # Asumiendo que existe en PacienteDB
        )

        id_cita = str(uuid.uuid4())
        nueva_cita = None
        if tipo_cita == "presencial":
            centro = data.get("centro")
            if not centro:
                return jsonify({"detail": "Para cita presencial, se requiere el centro."}), 400
            nueva_cita = gestor_de_citas.CitaPresencial(id_cita, paciente_obj, medico_asignado, fecha_hora_fmt_gestor, centro=centro, motivo=motivo)
        elif tipo_cita == "telefonica":
            telefono_contacto = data.get("telefono_contacto")
            if not telefono_contacto:
                return jsonify({"detail": "Para cita telefónica, se requiere el teléfono de contacto."}), 400
            nueva_cita = gestor_de_citas.CitaTelefonica(id_cita, paciente_obj, medico_asignado, fecha_hora_fmt_gestor, telefono_contacto=telefono_contacto, motivo=motivo)
        elif tipo_cita == "urgencias":
            nivel_prioridad = data.get("nivel_prioridad")
            if not nivel_prioridad:
                return jsonify({"detail": "Para cita de urgencias, se requiere el nivel de prioridad."}), 400
            nueva_cita = gestor_de_citas.CitaUrgencias(id_cita, paciente_obj, medico_asignado, fecha_hora_fmt_gestor, nivel_prioridad=nivel_prioridad, motivo=motivo)
        else:
            return jsonify({"detail": "Tipo de cita no válido. Opciones: presencial, telefonica, urgencias."}), 400

        if nueva_cita:
            try:
                gestor = gestor_de_citas.GestorCitas()  # Crea una instancia aquí
                gestor.anadir_cita(nueva_cita)
                return jsonify({"mensaje": f"Tu solicitud de cita {tipo_cita} ha sido registrada con ID: {id_cita}.", "id_cita": id_cita}), 201
            except Exception as e:
                error_message = f"Error al añadir la cita: {str(e)}"
                logging.error(error_message)
                return jsonify({"detail": error_message}), 500
        else:
            return jsonify({"detail": "Error al crear la cita."}), 500

    except Exception as e:
        db.rollback()
        logging.error(f"Error general al pedir cita: {str(e)}")
        return jsonify({"detail": f"Error al procesar la solicitud de cita: {str(e)}"}), 500
    finally:
        db.close()
# === Médicos CRUD ===
@app.route('/medicos', methods=['GET'])
def listar_medicos():
    db = next(get_db())
    medicos = db.query(MedicoDB).all()
    res = [{"id": m.id, "username": m.username, "especialidad": m.especialidad, "antiguedad": m.antiguedad} for m in medicos]
    return jsonify(res)

@app.route('/medicos/alta', methods=['POST'])
def alta_medico():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos."}), 400
    try:
        hashed_password = generate_password_hash(data['password'])
        nuevo_medico = MedicoDB(
            id=data['id'], username=data['username'], password=hashed_password,
            especialidad=data.get('especialidad'), antiguedad=data.get('antiguedad')
        )
        db = next(get_db())
        db.add(nuevo_medico)
        db.commit()
        return jsonify({"mensaje": "Médico dado de alta."}), 201
    except KeyError as e:
        db = next(get_db())
        db.rollback()
        return jsonify({"error": f"Campo requerido faltante: {str(e)}"}), 400
    except Exception as e:
        db = next(get_db())
        db.rollback()
        return jsonify({"error": str(e)}), 500
@app.route('/medicos/baja/<medico_id>', methods=['DELETE'])
def baja_medico(medico_id):
    db = next(get_db())
    medico = db.query(MedicoDB).filter(MedicoDB.id == medico_id).first()
    if not medico:
        return jsonify({"error": "Médico no existe."}), 404
    db.delete(medico)
    db.commit()
    return jsonify({"mensaje": "Médico eliminado."})

@app.route("/citas", methods=["GET"])
def listar_citas():
    citas = gestor_de_citas.mostrar_citas()
    return jsonify(citas)

# === Enfermeros CRUD ===
@app.route('/enfermeros', methods=['GET'])
def listar_enfermeros():
    db = next(get_db())
    enfermeros = db.query(EnfermeroDB).all()
    res = [{"id": e.id, "username": e.username, "antieguedad": e.antieguedad, "especialidad": e.especialidad} for e in enfermeros]
    return jsonify(res)

@app.route('/enfermeros/alta', methods=['POST'])
def alta_enfermero():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos."}), 400
    try:
        hashed_password = generate_password_hash(data['password'])
        nuevo_enfermero = EnfermeroDB(
            id=data['id'], username=data['username'], password=hashed_password,
            antieguedad=data.get('antieguedad'), especialidad=data.get('especialidad')
        )
        db = next(get_db())
        db.add(nuevo_enfermero)
        db.commit()
        return jsonify({"mensaje": "Enfermero dado de alta."}), 201
    except KeyError as e:
        db = next(get_db())
        db.rollback()
        return jsonify({"error": f"Campo requerido faltante: {str(e)}"}), 400
    except Exception as e:
        db = next(get_db())
        db.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/enfermeros/baja/<enf_id>', methods=['DELETE'])
def baja_enfermero(enf_id):
    db = next(get_db())
    enfermero = db.query(EnfermeroDB).filter(EnfermeroDB.id == enf_id).first()
    if not enfermero:
        return jsonify({"error": "Enfermero no existe."}), 404
    db.delete(enfermero)
    db.commit()
    return jsonify({"mensaje": "Enfermero eliminado."})

# === Auxiliares CRUD ===
@app.route('/auxiliares', methods=['GET'])
def listar_auxiliares():
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, antiguedad, id_enfermero FROM auxiliares")
    auxiliares = cursor.fetchall()
    conn.close()
    return jsonify([{"id": a[0], "antiguedad": a[1], "id_enfermero": a[2]} for a in auxiliares])

@app.route('/auxiliares/alta', methods=['POST'])
def alta_auxiliar():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos."}), 400
    try:
        conn = _conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO auxiliares (id, antiguedad, id_enfermero) VALUES (?, ?, ?)",
                       (data['id'], data['antiguedad'], data.get('id_enfermero')))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Auxiliar dado de alta."}), 201
    except KeyError as e:
        conn = _conectar_bd()
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Campo requerido faltante: {str(e)}"}), 400
    except sqlite3.IntegrityError as e:
        conn = _conectar_bd()
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Error de integridad: {str(e)}"}), 400

@app.route('/auxiliares/baja/<aux_id>', methods=['DELETE'])
def baja_auxiliar(aux_id):
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM auxiliares WHERE id=?", (aux_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"mensaje": "Auxiliar eliminado."})
    else:
        return jsonify({"error": "Auxiliar no existe."}), 404

# === Habitaciones CRUD ===
@app.route('/habitaciones', methods=['GET'])
def listar_habitaciones():
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT numero_habitacion, capacidad, limpia FROM habitaciones")
    habitaciones = cursor.fetchall()
    conn.close()
    return jsonify([{"numero": h[0], "capacidad": h[1], "limpia": bool(h[2])} for h in habitaciones])

@app.route('/habitaciones/alta', methods=['POST'])
def alta_habitacion():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos."}), 400
    try:
        conn = _conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habitaciones (numero_habitacion, capacidad, limpia) VALUES (?, ?, ?)",
                       (data['numero'], data['capacidad'], 0))  # Por defecto, la habitación está sucia (0)
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Habitación dada de alta."}), 201
    except KeyError as e:
        conn = _conectar_bd()
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Campo requerido faltante: {str(e)}"}), 400
    except sqlite3.IntegrityError as e:
        conn = _conectar_bd()
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Error de integridad: {str(e)}"}), 400

@app.route('/habitaciones/limpiar/<int:numero>', methods=['PATCH'])
def habitacion_limpiar(numero):
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE habitaciones SET limpia=1 WHERE numero_habitacion=?", (numero,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"mensaje": "Habitación limpiada."})
    else:
        return jsonify({"error": "Habitación no existe."}), 404

@app.route('/habitaciones/baja/<int:numero>', methods=['DELETE'])
def baja_habitacion(numero):
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habitaciones WHERE numero_habitacion=?", (numero,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"mensaje": "Habitación eliminada."})
    else:
        return jsonify({"error": "Habitación no existe."}), 404

# === Asignaciones 1:N ===
@app.route('/pacientes/asignar_medico', methods=['POST'])
def asignar_medico():
    data = request.get_json()
    if not data or 'id_paciente' not in data or 'id_medico' not in data:
        return jsonify({"error": "Se requieren id_paciente e id_medico."}), 400
    id_p = data['id_paciente']; id_m = data['id_medico']
    db = next(get_db())
    paciente = db.query(PacienteDB).filter(PacienteDB.id == id_p).first()
    medico = db.query(MedicoDB).filter(MedicoDB.id == id_m).first()
    if not paciente or not medico:
        return jsonify({"error": "Paciente o médico no existe."}), 404
    paciente.id_medico = id_m
    db.commit()
    return jsonify({"mensaje": "Médico asignado."})

@app.route('/pacientes/asignar_habitacion', methods=['POST'])
def asignar_habitacion():
    data = request.get_json()
    if not data or 'id_paciente' not in data or 'numero' not in data:
        return jsonify({"error": "Se requieren id_paciente y numero de habitación."}), 400
    id_p = data['id_paciente']; num = data['numero']
    db = next(get_db())
    paciente = db.query(PacienteDB).filter(PacienteDB.id == id_p).first()
    conn = _conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT numero_habitacion FROM habitaciones WHERE numero_habitacion=?", (num,))
    habitacion = cursor.fetchone()
    conn.close()
    if not paciente or not habitacion:
        return jsonify({"error": "Paciente o habitación no existe."}), 404
    paciente.id_habitacion = num
    db.commit()
    return jsonify({"mensaje": "Habitación asignada."})

# === Descargar PDF ===
@app.route('/paciente/descargar_pdf', methods=['GET'])
@requiere_autenticacion
def descargar_pdf(usuario):
    if usuario.rol != 'paciente':
        return jsonify({"error": "Acceso denegado."}), 403
    paciente_id = usuario.id
    db = next(get_db())
    paciente = db.query(PacienteDB).filter(PacienteDB.id == paciente_id).first()
    if not paciente:
        return jsonify({"error": "Paciente no existe."}), 404
    paciente_dict = {
        'id': paciente.id, 'username': paciente.username, 'nombre': paciente.nombre, 'apellido': paciente.apellido,
        'edad': paciente.edad, 'genero': paciente.genero, 'estado': paciente.estado, 'historial_medico': paciente.historial_medico,
        'id_enfermero': paciente.id_enfermero, 'id_medico': paciente.id_medico, 'id_habitacion': paciente.id_habitacion
    }
    try:
        nombre_pdf = generar_pdf_paciente(paciente_dict) # type: ignore[arg-type]
        return jsonify({"pdf": nombre_pdf})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoints de registro (Movidos al principio para claridad) ---

@app.route("/pacientes/register", methods=["POST"])
def register_paciente():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "No se proporcionaron datos de registro."}), 400
    username = None
    password = None
    nombre = None
    apellido = None
    edad = None
    genero = None
    estado = None
    hashed_password = None
    new_paciente = None
    db = next(get_db())
    try:
        username = data.get("username")
        password = data.get("password")
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        edad = data.get("edad")
        genero = data.get("genero")
        estado = data.get("estado")
        if not all([username, password, nombre, apellido, edad, genero, estado]):
            return jsonify({"detail": "Todos los campos son obligatorios."}), 400
        existing_user = db.query(PacienteDB).filter(PacienteDB.username == username).first()
        if existing_user:
            return jsonify({"detail": f"El username '{username}' ya está registrado."}), 409
        hashed_password = generate_password_hash(password)
        new_paciente = PacienteDB(id=username, username=username, password=hashed_password, nombre=nombre, apellido=apellido, edad=edad, genero=genero, estado=estado)
        db.add(new_paciente)
        db.commit()
        return jsonify({"message": f"Paciente '{username}' registrado exitosamente."}, 201)
    except Exception as e:
        db.rollback()
        return jsonify({"detail": f"Error al registrar el paciente: {str(e)}"}, 500)

@app.route("/medicos/register", methods=["POST"])
def register_medico():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "No se proporcionaron datos de registro."}), 400
    username = None
    password = None
    especialidad = None
    antiguedad = None
    id = None
    hashed_password = None
    new_medico = None
    db = next(get_db())
    try:
        username = data.get("username")
        password = data.get("password")
        especialidad = data.get("especialidad")
        antiguedad = data.get("antiguedad")
        id = data.get("id")
        if not all([username, password, especialidad, antiguedad, id]):
            return jsonify({"detail": "Todos los campos son obligatorios."}), 400
        existing_user = db.query(MedicoDB).filter(MedicoDB.username == username).first()
        if existing_user:
            return jsonify({"detail": f"El username '{username}' ya está registrado como médico."}), 409
        hashed_password = generate_password_hash(password)
        new_medico = MedicoDB(id=id, username=username, password=hashed_password, especialidad=especialidad, antiguedad=antiguedad)
        db.add(new_medico)
        db.commit()
        return jsonify({"message": f"Médico '{username}' registrado exitosamente."}, 201)
    except Exception as e:
        db.rollback()
        return jsonify({"detail": f"Error al registrar el médico: {str(e)}"}, 500)

@app.route("/enfermeros/register", methods=["POST"])
def register_enfermero():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "No se proporcionaron datos de registro."}), 400
    username = None
    password = None
    antieguedad = None
    especialidad = None
    id = None
    hashed_password = None
    new_enfermero = None
    db = next(get_db())
    try:
        username = data.get("username")
        password = data.get("password")
        antieguedad = data.get("antieguedad")
        especialidad = data.get("especialidad")
        id = data.get("id")
        if not all([username, password, antieguedad, especialidad, id]):
            return jsonify({"detail": "Todos los campos son obligatorios."}), 400
        existing_user = db.query(EnfermeroDB).filter(EnfermeroDB.username == username).first()
        if existing_user:
            return jsonify({"detail": f"El username '{username}' ya está registrado como enfermero."}), 409
        hashed_password = generate_password_hash(password)
        new_enfermero = EnfermeroDB(id=id, username=username, password=hashed_password, antieguedad=antieguedad, especialidad=especialidad)
        db.add(new_enfermero)
        db.commit()
        return jsonify({"message": f"Enfermero '{username}' registrado exitosamente."}, 201)
    except Exception as e:
        db.rollback()
        return jsonify({"detail": f"Error al registrar el enfermero: {str(e)}"}, 500)

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # Asegurar que las tablas SQLAlchemy se creen
    app.run(debug=True, port=5000)
