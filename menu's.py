import requests
import json
import os
import getpass  # Para entrada segura de contraseñas

# --- Configuración ---
BASE_URL = "http://127.0.0.1:5000"  # Asegúrate de que tu API de Flask esté corriendo en este puerto

# --- Variables Globales para la Sesión del Usuario ---
GLOBAL_USERNAME = None
GLOBAL_PASSWORD = None  # Se almacena en texto plano solo para la duración de la sesión CLI
GLOBAL_ROLE = None


# --- Funciones Auxiliares para Interacción con la API ---

def make_authenticated_request(method, endpoint, data=None, params=None):
    """
    Realiza una solicitud autenticada a la API de Flask.
    """
    headers = {"X-ROL": GLOBAL_ROLE} if GLOBAL_ROLE else {}
    auth = (GLOBAL_USERNAME, GLOBAL_PASSWORD) if GLOBAL_USERNAME and GLOBAL_PASSWORD else None
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, auth=auth, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, auth=auth, headers=headers, params=params)
        elif method == "DELETE":
            response = requests.delete(url, auth=auth, headers=headers, params=params)
        elif method == "PATCH":
            response = requests.patch(url, json=data, auth=auth, headers=headers, params=params)
        else:
            print(f"Método HTTP no soportado: {method}")
            return None

        response.raise_for_status()  # Lanza una excepción HTTPError para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP {e.response.status_code}: {e.response.json().get('detail', e.response.text)}")
        return None
    except requests.exceptions.ConnectionError:
        print("Error de conexión: Asegúrate de que la API de Flask esté en ejecución.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar la respuesta JSON: {response.text}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None


# --- Funciones de Menú Específicas por Rol ---

def mostrar_menu(opciones, titulo):
    """Muestra un menú y obtiene la selección del usuario."""
    print(f"\n--- {titulo} ---")
    for i, opcion in enumerate(opciones):
        print(f"{i + 1}. {opcion}")
    print("0. Salir")
    while True:
        try:
            eleccion = int(input("Selecciona una opción: "))
            if 0 <= eleccion <= len(opciones):
                return eleccion
            else:
                print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def menu_paciente():
    """Menú para usuarios con rol de Paciente."""
    global GLOBAL_USERNAME, GLOBAL_PASSWORD, GLOBAL_ROLE
    opciones = [
        "Pedir cita",
        "Descargar PDF de mi informe",
        "Buscar información de medicamento por nombre",
        "Ver información de mi SIP"
    ]
    while True:
        eleccion = mostrar_menu(opciones, "Menú de Paciente")
        if eleccion == 1:
            print("\n--- Pedir Cita ---")
            print("Tipos de cita disponibles: presencial, telefonica, urgencias")
            tipo_cita = input("Ingresa el tipo de cita: ").lower()
            fecha_hora_str = input("Fecha y hora de la cita (YYYY-MM-DDTHH:MM:SS, ej: 2025-06-01T10:30:00): ")
            medico_preferido = input("Médico preferido (opcional, dejar vacío si no aplica): ") or "Sin asignar"
            motivo_consulta = input("Motivo de la consulta (opcional): ") or ""

            data_cita = {
                "tipo_cita": tipo_cita,
                "fecha_hora": fecha_hora_str,
                "medico": medico_preferido,
                "motivo": motivo_consulta
            }

            if tipo_cita == "presencial":
                data_cita["centro"] = input("Centro de la cita: ")
            elif tipo_cita == "telefonica":
                data_cita["telefono_contacto"] = input("Teléfono de contacto: ")
            elif tipo_cita == "urgencias":
                data_cita["nivel_prioridad"] = input("Nivel de prioridad (ej: alta, media, baja): ")
            else:
                print("Tipo de cita no válido. Por favor, elige entre 'presencial', 'telefonica' o 'urgencias'.")
                continue # Volver al menú

            response = make_authenticated_request("POST", "/cita/pedir", data=data_cita)
            if response:
                print(response.get("mensaje", "Solicitud de cita enviada."))
            else:
                print("No se pudo enviar la solicitud de cita.")
        elif eleccion == 2:
            print("Descargando PDF de tu informe...")
            response = make_authenticated_request("GET", "/paciente/descargar_pdf")
            if response:
                print(f"PDF generado: {response.get('pdf', 'Nombre de archivo desconocido')}")
                print("Nota: Si la función `generar_pdf_paciente` usa un diálogo de guardado, este aparecerá.")
            else:
                print("No se pudo generar el PDF.")
        elif eleccion == 3:
            nombre_medicamento = input("Ingresa el nombre del medicamento a buscar: ")
            response = make_authenticated_request("GET", "/medicamento/info", params={'name': nombre_medicamento})
            if response:
                print("\n--- Información del Medicamento ---")
                if response.get('drugGroup'):
                    for concept_group in response['drugGroup'].get('conceptGroup', []):
                        for concept in concept_group.get('conceptProperties', []):
                            print(f"Nombre: {concept.get('name')}")
                            print(f"RxCUI: {concept.get('rxcui')}")
                            print("-" * 30)
                else:
                    print("No se encontró información para ese medicamento.")
            else:
                print("No se pudo obtener la información del medicamento.")
        elif eleccion == 4:
            response = make_authenticated_request("GET", "/paciente/mi_sip")
            if response:
                print("\n--- Información de tu SIP ---")
                for key, value in response.items():
                    print(f"{key.capitalize()}: {value}")
            else:
                print("No se pudo obtener la información de tu SIP.")
        elif eleccion == 0:
            print("Cerrando sesión de paciente.")
            GLOBAL_USERNAME = None
            GLOBAL_PASSWORD = None
            GLOBAL_ROLE = None
            break

def menu_medico():
    """Menú para usuarios con rol de Médico."""
    global GLOBAL_USERNAME, GLOBAL_PASSWORD, GLOBAL_ROLE
    opciones = [
        "Listar pacientes",
        "Listar médicos",
        "Listar enfermeros",
        "Listar auxiliares",
        "Dar de alta paciente",
        "Dar de baja paciente",
        "Dar de alta médico",
        "Dar de baja médico",
        "Dar de alta enfermero",
        "Dar de baja enfermero",
        "Dar de alta auxiliar",
        "Dar de baja auxiliar",
        "Asignar médico a paciente",
        "Asignar habitación a paciente",
        "Crear SIP para paciente",
        "Consultar SIP de paciente",
        "Eliminar SIP de paciente"
    ]
    while True:
        eleccion = mostrar_menu(opciones, "Menú de Médico")
        if eleccion == 1:
            response = make_authenticated_request("GET", "/pacientes")
            if response:
                print("\n--- Listado de Pacientes ---")
                for p in response:
                    print(
                        f"ID: {p['id']}, Nombre: {p['nombre']} {p['apellido']}, Edad: {p['edad']}, Estado: {p['estado']}")
            else:
                print("No se pudieron listar los pacientes.")
        elif eleccion == 2:
            response = make_authenticated_request("GET", "/medicos")
            if response:
                print("\n--- Listado de Médicos ---")
                for m in response:
                    print(
                        f"ID: {m['id']}, Username: {m['username']}, Especialidad: {m['especialidad']}, Antigüedad: {m['antiguedad']}")
            else:
                print("No se pudieron listar los médicos.")
        elif eleccion == 3:
            response = make_authenticated_request("GET", "/enfermeros")
            if response:
                print("\n--- Listado de Enfermeros ---")
                for e in response:
                    print(f"ID: {e['id']}, Username: {e['username']}")
            else:
                print("No se pudieron listar los enfermeros.")
        elif eleccion == 4:
            response = make_authenticated_request("GET", "/auxiliares")
            if response:
                print("\n--- Listado de Auxiliares ---")
                for a in response:
                    print(f"ID: {a['id']}, Antigüedad: {a['antiguedad']}, ID Enfermero: {a['id_enfermero']}")
            else:
                print("No se pudieron listar los auxiliares.")
        elif eleccion == 5:
            print("\n--- Alta de Paciente ---")
            try:
                paciente_data = {
                    "id": input("ID del paciente: "),
                    "username": input("Username: "),
                    "password": getpass.getpass("Contraseña: "),  # Se envía en texto plano al API
                    "nombre": input("Nombre: "),
                    "apellido": input("Apellido: "),
                    "edad": int(input("Edad: ")),
                    "genero": input("Género: "),
                    "estado": input("Estado: ")
                }
                response = make_authenticated_request("POST", "/pacientes/alta", data=paciente_data)
                if response:
                    print(response.get("mensaje", "Paciente dado de alta."))
            except ValueError:
                print("Entrada inválida para la edad. Por favor, ingresa un número.")
        elif eleccion == 6:
            paciente_id = input("ID del paciente a dar de baja: ")
            response = make_authenticated_request("DELETE", f"/pacientes/baja/{paciente_id}")
            if response:
                print(response.get("mensaje", "Paciente eliminado."))
        elif eleccion == 7:
            print("\n--- Alta de Médico ---")
            try:
                medico_data = {
                    "id": input("ID del médico: "),
                    "username": input("Username: "),
                    "password": getpass.getpass("Contraseña: "),  # Se envía en texto plano al API
                    "especialidad": input("Especialidad: "),
                    "antiguedad": int(input("Antigüedad (años): "))
                }
                response = make_authenticated_request("POST", "/medicos/alta", data=medico_data)
                if response:
                    print(response.get("mensaje", "Médico dado de alta."))
            except ValueError:
                print("Entrada inválida para la antigüedad. Por favor, ingresa un número.")
        elif eleccion == 8:
            medico_id = input("ID del médico a dar de baja: ")
            response = make_authenticated_request("DELETE", f"/medicos/baja/{medico_id}")
            if response:
                print(response.get("mensaje", "Médico eliminado."))
        elif eleccion == 9:
            print("\n--- Alta de Enfermero ---")
            try:
                enfermero_data = {
                    "id": input("ID del enfermero: "),
                    "username": input("Username: "),
                    "password": getpass.getpass("Contraseña: "),  # Se envía en texto plano al API
                    "antieguedad": int(input("Antigüedad (años): ")),  # Manteniendo el typo original 'antieguedad'
                    "especialidad": input("Especialidad: ")
                }
                response = make_authenticated_request("POST", "/enfermeros/alta", data=enfermero_data)
                if response:
                    print(response.get("mensaje", "Enfermero dado de alta."))
            except ValueError:
                print("Entrada inválida para la antigüedad. Por favor, ingresa un número.")
        elif eleccion == 10:
            enf_id = input("ID del enfermero a dar de baja: ")
            response = make_authenticated_request("DELETE", f"/enfermeros/baja/{enf_id}")
            if response:
                print(response.get("mensaje", "Enfermero eliminado."))
        elif eleccion == 11:
            print("\n--- Alta de Auxiliar ---")
            try:
                auxiliar_data = {
                    "id": input("ID del auxiliar: "),
                    "antiguedad": int(input("Antigüedad (años): ")),
                    "id_enfermero": input("ID del enfermero (opcional, dejar vacío si no aplica): ") or None
                }
                response = make_authenticated_request("POST", "/auxiliares/alta", data=auxiliar_data)
                if response:
                    print(response.get("mensaje", "Auxiliar dado de alta."))
            except ValueError:
                print("Entrada inválida para la antigüedad. Por favor, ingresa un número.")
        elif eleccion == 12:
            aux_id = input("ID del auxiliar a dar de baja: ")
            response = make_authenticated_request("DELETE", f"/auxiliares/baja/{aux_id}")
            if response:
                print(response.get("mensaje", "Auxiliar eliminado."))
        elif eleccion == 13:
            print("\n--- Asignar Médico a Paciente ---")
            data = {
                "id_paciente": input("ID del paciente: "),
                "id_medico": input("ID del médico: ")
            }
            response = make_authenticated_request("POST", "/pacientes/asignar_medico", data=data)
            if response:
                print(response.get("mensaje", "Médico asignado."))
        elif eleccion == 14:
            print("\n--- Asignar Habitación a Paciente ---")
            try:
                data = {
                    "id_paciente": input("ID del paciente: "),
                    "numero": int(input("Número de habitación: "))
                }
                response = make_authenticated_request("POST", "/pacientes/asignar_habitacion", data=data)
                if response:
                    print(response.get("mensaje", "Habitación asignada."))
            except ValueError:
                print("Entrada inválida para el número de habitación. Por favor, ingresa un número.")
        elif eleccion == 15:
            paciente_id = input("ID del paciente para crear SIP: ")
            response = make_authenticated_request("GET", f"/crear_sip/{paciente_id}")
            if response:
                print(f"SIP creado: {response.get('sip', 'N/A')}")
            else:
                print("No se pudo crear el SIP.")
        elif eleccion == 16:
            paciente_id = input("ID del paciente para consultar SIP: ")
            response = make_authenticated_request("GET", f"/consultar_sip/{paciente_id}")
            if response:
                print(f"SIP: {response.get('sip', 'No encontrado')}")
            else:
                print("No se pudo consultar el SIP.")
        elif eleccion == 17:
            paciente_id = input("ID del paciente para eliminar SIP: ")
            response = make_authenticated_request("DELETE", f"/eliminar_sip/{paciente_id}")
            if response:
                print(response.get("mensaje", "SIP eliminado."))
            else:
                print("No se pudo eliminar el SIP.")
        elif eleccion == 0:
            print("Cerrando sesión de médico.")
            GLOBAL_USERNAME = None
            GLOBAL_PASSWORD = None
            GLOBAL_ROLE = None
            break

def menu_enfermero():
    """Menú para usuarios con rol de Enfermero."""
    global GLOBAL_USERNAME, GLOBAL_PASSWORD, GLOBAL_ROLE
    opciones = [
        "Listar pacientes",
        "Listar enfermeros",
        "Listar habitaciones",
        "Listar auxiliares",
        "Dar de alta enfermero",
        "Dar de baja enfermero",
        "Dar de alta auxiliar",
        "Dar de baja auxiliar",
        "Dar de alta habitación",
        "Dar de baja habitación",
        "Limpiar habitación"
    ]
    while True:
        eleccion = mostrar_menu(opciones, "Menú de Enfermero")
        if eleccion == 1:
            response = make_authenticated_request("GET", "/pacientes")
            if response:
                print("\n--- Listado de Pacientes ---")
                for p in response:
                    print(
                        f"ID: {p['id']}, Nombre: {p['nombre']} {p['apellido']}, Edad: {p['edad']}, Estado: {p['estado']}")
            else:
                print("No se pudieron listar los pacientes.")
        elif eleccion == 2:
            response = make_authenticated_request("GET", "/enfermeros")
            if response:
                print("\n--- Listado de Enfermeros ---")
                for e in response:
                    print(f"ID: {e['id']}, Username: {e['username']}")
            else:
                print("No se pudieron listar los enfermeros.")
        elif eleccion == 3:
            response = make_authenticated_request("GET", "/habitaciones")
            if response:
                print("\n--- Listado de Habitaciones ---")
                for h in response:
                    print(f"Número: {h['numero']}, Capacidad: {h['capacidad']}, Limpia: {h['limpia']}")
            else:
                print("No se pudieron listar las habitaciones.")
        elif eleccion == 4:
            response = make_authenticated_request("GET", "/auxiliares")
            if response:
                print("\n--- Listado de Auxiliares ---")
                for a in response:
                    print(f"ID: {a['id']}, Antigüedad: {a['antiguedad']}, ID Enfermero: {a['id_enfermero']}")
            else:
                print("No se pudieron listar los auxiliares.")
        elif eleccion == 5:
            print("\n--- Alta de Enfermero ---")
            try:
                enfermero_data = {
                    "id": input("ID del enfermero: "),
                    "username": input("Username: "),
                    "password": getpass.getpass("Contraseña: "),  # Se envía en texto plano al API
                    "antieguedad": int(input("Antigüedad (años): ")),  # Manteniendo el typo original 'antieguedad'
                    "especialidad": input("Especialidad: ")
                }
                response = make_authenticated_request("POST", "/enfermeros/alta", data=enfermero_data)
                if response:
                    print(response.get("mensaje", "Enfermero dado de alta."))
            except ValueError:
                print("Entrada inválida para la antigüedad. Por favor, ingresa un número.")
        elif eleccion == 6:
            enf_id = input("ID del enfermero a dar de baja: ")
            response = make_authenticated_request("DELETE", f"/enfermeros/baja/{enf_id}")
            if response:
                print(response.get("mensaje", "Enfermero eliminado."))
        elif eleccion == 7:
            print("\n--- Alta de Auxiliar ---")
            try:
                auxiliar_data = {
                    "id": input("ID del auxiliar: "),
                    "antiguedad": int(input("Antigüedad (años): ")),
                    "id_enfermero": input("ID del enfermero (opcional, dejar vacío si no aplica): ") or None
                }
                response = make_authenticated_request("POST", "/auxiliares/alta", data=auxiliar_data)
                if response:
                    print(response.get("mensaje", "Auxiliar dado de alta."))
            except ValueError:
                print("Entrada inválida para la antigüedad. Por favor, ingresa un número.")
        elif eleccion == 8:
            aux_id = input("ID del auxiliar a dar de baja: ")
            response = make_authenticated_request("DELETE", f"/auxiliares/baja/{aux_id}")
            if response:
                print(response.get("mensaje", "Auxiliar eliminado."))
        elif eleccion == 9:
            print("\n--- Alta de Habitación ---")
            try:
                habitacion_data = {
                    "numero": int(input("Número de habitación: ")),
                    "capacidad": int(input("Capacidad: "))
                }
                response = make_authenticated_request("POST", "/habitaciones/alta", data=habitacion_data)
                if response:
                    print(response.get("mensaje", "Habitación dada de alta."))
            except ValueError:
                print("Entrada inválida para número o capacidad. Por favor, ingresa números.")
        elif eleccion == 10:
            try:
                numero_hab = int(input("Número de habitación a dar de baja: "))
                response = make_authenticated_request("DELETE", f"/habitaciones/baja/{numero_hab}")
                if response:
                    print(response.get("mensaje", "Habitación eliminada."))
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
        elif eleccion == 11:
            try:
                numero_hab = int(input("Número de habitación a limpiar: "))
                response = make_authenticated_request("PATCH", f"/habitaciones/limpiar/{numero_hab}")
                if response:
                    print(response.get("mensaje", "Habitación limpiada."))
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
        elif eleccion == 0:
            print("Cerrando sesión de enfermero.")
            GLOBAL_USERNAME = None
            GLOBAL_PASSWORD = None
            GLOBAL_ROLE = None
            break
# --- Función de Inicio de Sesión ---

def login():
    """
    Maneja el proceso de inicio de sesión del usuario.
    """
    global GLOBAL_USERNAME, GLOBAL_PASSWORD, GLOBAL_ROLE
    print("\n--- Inicio de Sesión ---")
    username = input("Username: ")
    password = getpass.getpass("Contraseña: ")  # getpass para entrada segura sin eco
    rol = input("Rol (paciente/medico/enfermero): ").lower()

    if rol not in ['paciente', 'medico', 'enfermero']:
        print("Rol no válido. Por favor, elige 'paciente', 'medico' o 'enfermero'.")
        return False

    # Intentar autenticar llamando a un endpoint protegido (ej. /menu)
    # La API de Flask usará el decorador requiere_autenticacion para validar.
    headers = {"X-ROL": rol}
    auth = (username, password)

    try:
        response = requests.get(f"{BASE_URL}/menu", auth=auth, headers=headers)
        response.raise_for_status()  # Lanza HTTPError para 4xx/5xx

        # Si la autenticación es exitosa, la API devuelve el menú.
        # Almacenamos las credenciales para futuras solicitudes.
        GLOBAL_USERNAME = username
        GLOBAL_PASSWORD = password
        GLOBAL_ROLE = rol
        print(f"Inicio de sesión exitoso como {rol}!")
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Credenciales inválidas o rol incorrecto.")
        elif e.response.status_code == 403:
            print("Acceso denegado para este rol.")
        else:
            print(f"Error HTTP {e.response.status_code}: {e.response.json().get('detail', e.response.text)}")
        return False
    except requests.exceptions.ConnectionError:
        print("Error de conexión: Asegúrate de que la API de Flask esté en ejecución.")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado durante el inicio de sesión: {e}")
        return False


# --- Bucle Principal de la Aplicación CLI ---

def main():
    """
    Función principal de la aplicación CLI.
    """
    global GLOBAL_USERNAME, GLOBAL_PASSWORD, GLOBAL_ROLE
    while True:
        if GLOBAL_USERNAME is None:  # No logueado
            print("\n--- Bienvenid@ la Aplicación Hospitalaria de ProSalud ---")
            print("1. Iniciar Sesión")
            print("0. Salir de la Aplicación")
            choice = input("Selecciona una opción: ")
            if choice == '1':
                if login():
                    if GLOBAL_ROLE == 'paciente':
                        menu_paciente()
                    elif GLOBAL_ROLE == 'medico':
                        menu_medico()
                    elif GLOBAL_ROLE == 'enfermero':
                        # El menú de enfermero no está detallado en la API,
                        # pero se puede añadir siguiendo el mismo patrón.
                        print("Menú de enfermero no implementado en esta versión CLI.")
                        GLOBAL_USERNAME = None  # Forzar logout si no hay menú
                        GLOBAL_PASSWORD = None
                        GLOBAL_ROLE = None
            elif choice == '0':
                print("Saliendo de la aplicación. ¡Hasta pronto!")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")
        else:  # Ya logueado, pero el menú específico ya maneja el logout.
            # Esto es más un fallback si el usuario no sale del menú específico.
            print("Ya has iniciado sesión. Por favor, sal del menú actual para cambiar de usuario o salir.")
            if GLOBAL_ROLE == 'paciente':
                menu_paciente()
            elif GLOBAL_ROLE == 'medico':
                menu_medico()
            elif GLOBAL_ROLE == 'enfermero':
                print("Menú de enfermero no implementado en esta versión CLI.")
                GLOBAL_USERNAME = None  # Forzar logout si no hay menú
                GLOBAL_PASSWORD = None
                GLOBAL_ROLE = None


if __name__ == "__main__":
    main()