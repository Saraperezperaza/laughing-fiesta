# calendario_vacunacion.py
# importo datetime(ahora mismo no lo estoy usando), lo he importado para
# ver si queremos agregar fechas de vacunación o un historial

# en esta clase nos encargamos de gestionar y recomendar vacunas a los pacientes
# para ello nos basámos en la edad y condiciones especiales como las alergías
class CalendarioVacunacion:
    def __init__(self):
        # Definimos las vacunas por edad o tipo
        # para ello usamos un diccionario de vacunas para distintos rangos de edad
        # o distintas condiciones como:
        # 18-pacientes de 18 años exactos
        # 60-personas mayores de 60 años
        # menor-para menores de edad(menos de 18)
        # alergico-si tienen alguna alergía
        # el diccionario es la base para todas las recomendaciones
        self.vacunas = {
            18: ["Vacuna Hepatitis B", "Vacuna Triple Viral"],
            60: ["Vacuna Neumocócica", "Vacuna Meningitis"],
            "menor": ["Vacuna DTP", "Vacuna Polio", "Vacuna MMR"],
            "alergico": ["Vacuna antialérgica", "Vacuna para asma"]
        }

    # Méodo para determinar la próxima vacuna según la edad y condiciones del paciente
    # tomamos un objeto paciente y extrae su edad
    # verificamos si el paciente tiene el atributo alergias
    # inicializamos una lista vacía vacunas_recomendadas

    def obtener_vacunas(self, paciente):
        edad = paciente.edad
        alergias = paciente.alergias if hasattr(paciente, 'alergias') else None

        vacunas_recomendadas = []

        # Recomendaciones según edad
        # si el paciente es menor de edad, se añaden vacunas pediátricas
        # si es mayor o igual a 60 , se añaden vacunas recomendadas para adultos mayores

        if edad < 18:
            vacunas_recomendadas += self.vacunas["menor"]
        if edad >= 60:
            vacunas_recomendadas += self.vacunas[60]

        # Si tiene alergias
        # y si la palabra alergia aparece en la lista se le asignan vacunas especiales
        if alergias and "alergia" in alergias:
            vacunas_recomendadas += self.vacunas["alergico"]

        # Recomendación según edad exacta
        # si hay una edad específica como 18 o 60 años
        # se suman esas vacunas también
        if edad in self.vacunas:
            vacunas_recomendadas += self.vacunas[edad]
        # devuelve una lista con todas las vacunas recomendadas
        return vacunas_recomendadas

    # Mostrar calendario de vacunación
    # llama al méodo anterior(obtener_vacunas) para obtener las vacunas del paciente
    # - si hay vacunas:
    # imprime un encabezado con el nombre del paciente
    # vemos la lista de cada vacuna en consola
    # - si no hay vacunas
    # imprime un mensaje avisando que no hay recomendaciones actuales
    def mostrar_calendario(self, paciente):
        vacunas = self.obtener_vacunas(paciente)
        if vacunas:
            print(f"Calendario de vacunación para {paciente.nombre}:")
            for vacuna in vacunas:
                print(f"- {vacuna}")
        else:
            print(f"No hay vacunas recomendadas para {paciente.nombre} en este momento.")