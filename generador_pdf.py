from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Clases_Base_de_datos.paciente import Paciente  # Importamos la clase Paciente para tipado

def generar_pdf_paciente(paciente: Paciente) -> str:

    nombre_archivo = f"Informe del Paciente_{paciente.id, paciente.username}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Informe Personal del Paciente")

    # Información del paciente
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(100, y, f"Nombre: {paciente._nombre}")
    y -= 20
    c.drawString(100, y, f"Edad: {paciente.edad}")
    y -= 20
    c.drawString(100, y, f"Username: {paciente.username}")
    y -= 20
    c.drawString(100, y, f"Enfermedades: {paciente.enfermedades}")
    y -= 20
    c.drawString(100, y, f"Tipo de Prioridad en Urgencias: {paciente.prioridad_urgencias}")
    y -= 20
    c.drawString(100, y, f"Alergias: {paciente.alergias}")

    # Historial médico
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Historial Médico")
    c.setFont("Helvetica", 12)
    y -= 20
    if paciente.historial_medico:
        for entrada in paciente.historial_medico:
            c.drawString(100, y, entrada)
            y -= 20
    else:
        c.drawString(100, y, "No hay entradas en el historial médico.")
        y -= 20

    # Citas
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Citas")
    c.setFont("Helvetica", 12)
    y -= 20
    if paciente.citas:
        for cita in paciente.citas:
            c.drawString(100, y, f"Fecha: {cita.fecha_hora_dt}, Médico: {cita.medico}, Motivo: {cita.motivo}")
            y -= 20
    else:
        c.drawString(100, y, "No hay citas programadas.")
        y -= 20

    c.save()
    return nombre_archivo