# manejo_habitaciones.py
from Base_De_Datos.tablas.tabla_habitacion import crear_tabla_habitaciones, leer_habitaciones, insertar_habitacion, limpiar_habitacion
from Base_De_Datos.tablas.tabla_enfermero import crear_tabla_enfermeros, leer_enfermeros
from Base_De_Datos.tablas.tabla_paciente import crear_tabla_pacientes, eliminar_paciente, leer_pacientes
class ManejoHabitaciones:
    def __init__(self):
        crear_tabla_habitaciones()
        crear_tabla_enfermeros()
        crear_tabla_pacientes()
        self.habitaciones = {
            num: {'capacidad': cap, 'limpia': bool(limp)}
            for num, cap, limp in leer_habitaciones()
        } # Diccionario para almacenar habitaciones: {numero_habitacion: Habitacion}
        self.asignaciones = {}    # Diccionario para almacenar enfermeros asignados: {numero_habitacion: Enfermero}
        self.enfermeros = {id_enf: { 'nombre': nombre }
            for id_enf, nombre in leer_enfermeros()
        }
        self.pacientes_habitacion = {}
        for num, habitacion_id in leer_pacientes():
            self.pacientes_habitacion.setdefault(num, []).append(habitacion_id)
    def agregar_habitacion(self, numero_habitacion: int, capacidad: int)->None:
        """Agrega una habitación al sistema."""
        if numero_habitacion in self.habitaciones:
            raise ValueError(f"La habitación {numero_habitacion} ya existe.")
        insertar_habitacion(numero_habitacion, capacidad)
        self.habitaciones[numero_habitacion] = {'capacidad': capacidad, 'limpia': False}
        print(f"Habitación {numero_habitacion} agregada con capacidad {capacidad}.")

    def asignar_habitacion_a_enfermero(self, numero_habitacion:int, enfermero_id:str)->None:
        """Asigna una habitación a un enfermero."""
        if numero_habitacion not in self.habitaciones:
            raise ValueError(f"Habitación {numero_habitacion} no registrada.")
        if enfermero_id not in self.enfermeros:
            raise ValueError(f"Enfermero {enfermero_id} no existe.")
        self.asignaciones[numero_habitacion] = enfermero_id
        print(f"Habitación {numero_habitacion} asignada a enfermero {enfermero_id}.")

    def limpiar_habitacion(self, numero_habitacion:int)->None:
        """Limpia una habitación específica, verificando que el enfermero esté asignado."""
        if numero_habitacion not in self.habitaciones:
            raise ValueError(f"Habitación {numero_habitacion} no registrada.")
        limpiar_habitacion(numero_habitacion)
        self.habitaciones[numero_habitacion]['limpia'] = True
        print(f"Habitación {numero_habitacion} marcada como limpia.")


    def asignar_paciente_a_habitacion(self, paciente_id, numero_habitacion:int)->None:
        """Asigna un paciente a una habitación específica, verificando limpieza y capacidad."""
        if numero_habitacion not in self.habitaciones:
            raise ValueError(f"Habitación {numero_habitacion} no registrada.")
        estado = self.habitaciones[numero_habitacion]
        if not estado['limpia']:
            raise ValueError(f"Habitación {numero_habitacion} sucia; límpiela primero.")
        lst = self.pacientes_habitacion.setdefault(numero_habitacion, [])
        if len(lst) >= estado['capacidad']:
            raise ValueError(f"Habitación {numero_habitacion} llena.")
        lst.append(paciente_id)
        print(f"Paciente {paciente_id} asignado a habitación {numero_habitacion}.")
    def eliminar_paciente_de_habitacion(self, paciente_id:str, numero_habitacion:int):
        """Elimina un paciente de una habitación específica."""
        habs = self.pacientes_habitacion.get(numero_habitacion)
        if not habs or paciente_id not in habs:
            raise ValueError(f"Paciente {paciente_id} no está en habitación {numero_habitacion}.")
        else:
            eliminar_paciente(paciente_id)
            habs.remove(paciente_id)
        print(f"Paciente {paciente_id} eliminado de habitación {numero_habitacion}.")

    def buscar_habitacion(self, numero_habitacion:int):
        """Busca una habitación por su número."""
        return self.habitaciones.get(numero_habitacion)

    def mostrar_habitaciones(self, enfermero):
        """Muestra información de las habitaciones asignadas a un enfermero."""
        habitaciones_asignadas = [
            numero for numero, enf in self.enfermeros.items() if enf == enfermero]
        if not habitaciones_asignadas:
            return "No hay habitaciones asignadas a este enfermero"
        info = "Habitaciones asignadas:\n"
        for numero in habitaciones_asignadas:
            estado = self.habitaciones[numero]
            pacientes = self.pacientes_habitacion.get(numero, [])
            info += (f"Hab {numero}: capacidad={estado['capacidad']}, limpia={estado['limpia']}, "
                     f"pacientes={pacientes}\n")
        return info.rstrip('\n')

    def mostrar_todas_habitaciones(self):
        """Muestra información de todas las habitaciones en el sistema."""
        if not self.habitaciones:
            return "No hay habitaciones registradas en el sistema"
        info = "Habitaciones en el sistema:\n"
        for numero,estado in self.habitaciones.items():
            enfermero = self.enfermeros.get(numero, "Ninguno")
            pacientes = self.pacientes_habitacion.get(numero, [])
            info += (f"Hab {numero}: cap={estado['capacidad']}, limpia={estado['limpia']}, "
                     f"enfermero={enfermero}, pacientes={pacientes}")
        return info.rstrip('\n')