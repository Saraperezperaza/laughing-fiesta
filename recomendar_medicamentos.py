"""
Funciones para recomendar medicamentos basadas en síntomas y alergias.
"""
from typing import Union, List
import json
import datetime
from Base_De_Datos.tablas.tabla_paciente    import (
    crear_tabla_pacientes,
    crear_tabla_paciente_enfermedad,
    leer_pacientes
)
from Base_De_Datos.tablas.tabla_medicamento import (
    crear_tabla_medicamentos,
    leer_medicamentos
)

from Clases_Base_de_datos.paciente   import Paciente
from Clases_Base_de_datos.medicamento import Medicamento

crear_tabla_pacientes()
crear_tabla_paciente_enfermedad()
crear_tabla_medicamentos()

pacientes_filas = leer_pacientes()
medicamentos_filas = leer_medicamentos()

pacientes: List[Paciente] = [
    Paciente(  # ajusta el constructor según tu clase
        id=row[0],
        username=row[1],
        password=row[2],
        nombre=row[3],
        apellido=row[4],
        edad=row[5],
        genero=row[6],
        estado=row[7],
        historial_medico=json.loads(row[8]) if row[8] else None
    )
    for row in pacientes_filas
]
medicamentos: List[Medicamento] = [
    Medicamento(
        id=row[0],
        nombre=row[1],
        dosis=row[2],
        precio=row[3],
        fecha_caducidad=datetime.datetime.fromisoformat(row[4]),
        alergenos=row[5].split(',') if row[5] else []
    )
    for row in medicamentos_filas
]

def recomendar_medicamento(
    paciente: Paciente,
    lista_medicamentos: List[Medicamento]
) -> List[Medicamento]:
    sintomas_paciente = []
    for enf in paciente.enfermedades:
        sintomas_paciente.extend(enf.sintomas)

    if not sintomas_paciente:
        raise ValueError("El paciente no tiene síntomas")

    adecuados = []
    for med in lista_medicamentos:
        if any(s in med.sintomas_curables for s in sintomas_paciente):
            adecuados.append(med)

    if paciente.alergias:
        filtrados = []
        for med in adecuados:
            if not any(a in med.alergenos for a in paciente.alergias):
                filtrados.append(med)
        return filtrados
    return adecuados

def comprobacion_alergenos(
    paciente: Paciente,
    meds: Union[Medicamento, List[Medicamento]]
) -> dict[str,str]:
    resultado = {}
    lista = [meds] if isinstance(meds, Medicamento) else meds
    if not paciente.alergias:
        raise ValueError("El paciente no tiene alergias")

    for med in lista:
        clave = "Contiene alérgenos" if any(a in med.alergenos for a in paciente.alergias) else "Seguro"
        resultado[med.nombre] = clave
    return resultado

if __name__ == "__main__":
    crear_tabla_pacientes()
    crear_tabla_paciente_enfermedad()
    crear_tabla_medicamentos()

    if not pacientes:
        print("No hay pacientes. Inserta alguno con 'insertar_paciente()' y vuelve a intentarlo.")
        exit(1)
    if not medicamentos:
        print("No hay medicamentos. Inserta alguno con 'insertar_medicamento()' y vuelve a intentarlo.")
        exit(1)

    p = pacientes[0]
    rec = recomendar_medicamento(p, medicamentos)
    print("Recomendados:", [m.nombre for m in rec])
    print("Alergias:", comprobacion_alergenos(p, rec))
