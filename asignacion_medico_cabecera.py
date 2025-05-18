import random
import sqlite3
from typing import List
from Clases_Base_de_datos.medico import Medico
from Clases_Base_de_datos.paciente import Paciente
from Base_De_Datos.tablas.tabla_asignaciones import conectar, crear_tabla_asignaciones

class Asignaciones:

    """
    Clase encargada de gestionar la asignación de médicos a paciente

    """

    def __init__(self, medicos : List[Medico], pacientes: List[Paciente]):

        """
            Parámetros:
            -----------

            Inicializa el gestor con una lista de médicos disponibles

            medicos: Lista de instancias de la clase Médico
            pacientes: Lista de instancias de la clase Paciente

        """
        crear_tabla_asignaciones()
        self.medicos = {m.id: m for m in medicos}
        self.pacientes = {p.id: p for p in pacientes}

    def cambiar_disponibilidad(self, medico_id :str, disponible :bool) -> None:

        """
                Cambia la disponibilidad de un médico dado su ID.

                medico_id: ID del médico al que se desea cambiar la disponibilidad.
                disponible: True si el médico debe estar disponible, False si no.
        """
        m = self.medicos.get(medico_id)
        if m:
            m.disponibilidad = disponible
            print(f"Disponibilidad de {m.nombre} actualizada a {disponible}.")
        else:
            print("No se encontró un médico con ese ID.")

    def medicos_disponibles(self) -> List[Medico]:

        """
            Devuelve una lista con los médicos disponibles

        """
        return [m for m in self.medicos.values() if getattr(m, 'disponibilidad', True)]

    def asignar(self, paciente_id: str) -> bool or None:

        """
            Asigna aleatoriamente un médico disponible a un paciente.
            Retorna True si se realizó la asignación con éxito

        """

        if paciente_id not in self.pacientes:
            print("Paciente no encontrado.")
            return False

        disponibles = self.medicos_disponibles()
        if not disponibles:
            print("No hay médicos disponibles.")
            return False

        medico = random.choice(disponibles)
        conn = conectar()
        try:
            conn.execute(
                "INSERT INTO asignaciones (paciente_id, medico_id) VALUES (?, ?)",
                (paciente_id, medico.id)
            )
            conn.commit()
            print(f"Paciente {self.pacientes[paciente_id].nombre} - Médico {medico.nombre}")
            return True
        except sqlite3.IntegrityError as e:
            print("Error al asignar:", e)
            return False
        finally:
            conn.close()

    def mostrar_asignaciones(self) -> None:

        """
            Muestra todas las asignaciones realizadas

        """

        sql = '''
                SELECT a.id, p.nombre, p.apellido, m.nombre, m.apellido
                  FROM asignaciones a
                  JOIN pacientes p ON a.paciente_id = p.id
                  JOIN medicos   m ON a.medico_id   = m.id
                '''
        conn = conectar()
        for _id, pnom, pap, mnom, map_ in conn.execute(sql):
            print(f"[{_id}] Paciente: {pnom} {pap}  ←→  Médico: {mnom} {map_}")
        conn.close()
