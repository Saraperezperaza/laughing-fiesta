from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Clases_Base_de_datos.paciente import Paciente  # Importamos la clase Paciente para tipado
import tkinter as tk
from tkinter import filedialog
import os

# Importamos os para manejar rutas de archivo

def generar_pdf_paciente(paciente: Paciente) -> str:
    """
    Genera un informe PDF detallado para un paciente dado, permitiendo al usuario
    elegir la ruta donde guardar el archivo.

    Args:
        paciente (Paciente): Un objeto Paciente con la información a incluir en el PDF.

    Returns:
        str: La ruta completa del archivo PDF generado, o una cadena vacía si la operación
             fue cancelada por el usuario.
    """

    # Ocultar la ventana principal de Tkinter que se crea por defecto
    root = tk.Tk()
    root.withdraw()

    # Generar un nombre de archivo sugerido
    nombre_sugerido = f"Informe_del_Paciente_{paciente.id}_{paciente.username}.pdf"

    # Abrir el diálogo para guardar el archivo
    # Se le pide al usuario que seleccione una ubicación y un nombre para el archivo.
    # El valor inicial del nombre de archivo se establece para facilitar al usuario.
    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=nombre_sugerido,
        title="Guardar Informe del Paciente como...",
        filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
    )

    # Si el usuario cancela el diálogo, no se genera el PDF
    if not ruta_guardado:
        print("Operación de guardado de PDF cancelada por el usuario.")
        return ""

    # Crear el objeto Canvas con la ruta de guardado seleccionada
    c = canvas.Canvas(ruta_guardado, pagesize=letter)
    width, height = letter

    # Título del informe
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Informe Personal del Paciente")

    # Información del paciente
    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(100, y, f"Nombre: {paciente.nombre}")
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
            # Asegurarse de que el texto no exceda el ancho de la página
            # Se puede añadir lógica para envolver el texto si es muy largo
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

    # Guardar el PDF
    c.save()

    # Devolver la ruta completa del archivo guardado
    return ruta_guardado
