import random
from typing import List
from Base_De_Datos.tablas.tabla_asignaciones import crear_tabla_asignaciones, insertar_asignacion, leer_asignaciones
from Base_De_Datos.tablas.tabla_paciente import crear_tabla_pacientes, leer_pacientes
from Base_De_Datos.tablas.tabla_medico import crear_tabla_medicos, leer_medicos

class Asignaciones:
    """
    Gestiona asignaciones médico–paciente usando directamente las tablas SQLite.
    """

    def __init__(self) -> None:
        # Crear tablas si no existen
        crear_tabla_pacientes()
        crear_tabla_medicos()
        crear_tabla_asignaciones()
        # Cargar datos en memoria: id -> (nombre, apellido)
        self.pacientes: dict = {
            pid: (nombre, apellido)
            for pid, _, _, nombre, apellido, *_ in leer_pacientes()
        }
        # Cargar médicos en memoria: id -> username
        self.medicos: dict[str, str] = {
            mid: username
            for mid, username, *_ in leer_medicos()
        }

    def medicos_disponibles(self) -> List:
        """
        Devuelve lista de médicos disponibles como lista de tuplas (medico_id, username).
        """
        return list(self.medicos.items())

    def asignar(self, paciente_id: str) -> bool:
        """
        Asigna aleatoriamente un médico a un paciente y guarda la relación en la tabla.
        """
        datos_paciente = self.pacientes.get(paciente_id)
        if not datos_paciente:
            print("Paciente no encontrado.")
            return False

        disponibles = self.medicos_disponibles()
        if not disponibles:
            print("No hay médicos disponibles.")
            return False

        medico_id, medico_user = random.choice(disponibles)
        try:
            insertar_asignacion(paciente_id, medico_id)
            print(f"Paciente {datos_paciente[0]} {datos_paciente[1]} ←→ Médico {medico_user}")
            return True
        except Exception as e:
            print("Error al asignar:", e)
            return False

    def mostrar_asignaciones(self) -> None:
        """
        Muestra todas las asignaciones con nombre/apellido de paciente y username de médico.
        """
        for asign_id, pid, mid in leer_asignaciones():
            nombre_p, apellido_p = self.pacientes.get(pid, ("(desconocido)", ""))
            medico_user = self.medicos.get(mid, "(desconocido)")
            print(f"[{asign_id}] Paciente: {nombre_p} {apellido_p}  ←→  Médico: {medico_user}")
