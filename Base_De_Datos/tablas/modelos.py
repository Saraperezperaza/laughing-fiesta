from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PacienteDB(Base):
    __tablename__ = 'pacientes'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    edad = Column(Integer)
    genero = Column(String)
    estado = Column(String)
    historial_medico = Column(Text)
    id_enfermero = Column(String, ForeignKey('enfermeros.id'))
    id_medico = Column(String, ForeignKey('medicos.id'))
    id_habitacion = Column(Integer, ForeignKey('habitaciones.numero_habitacion'))

    enfermero = relationship("EnfermeroDB", back_populates="pacientes")
    medico = relationship("MedicoDB", back_populates="pacientes")
    habitacion = relationship("HabitacionDB", back_populates="pacientes")
    sip = relationship("SipDB", back_populates="paciente", uselist=False)
    citas = relationship("CitaDB", back_populates="paciente")

class MedicoDB(Base):
    __tablename__ = 'medicos'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    especialidad = Column(String)
    antiguedad = Column(Integer)

    pacientes = relationship("PacienteDB", back_populates="medico")
    citas = relationship("CitaDB", back_populates="medico")

class EnfermeroDB(Base):
    __tablename__ = 'enfermeros'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    antiguedad = Column(Integer, nullable=False)
    especialidad = Column(String)

    pacientes = relationship("PacienteDB", back_populates="enfermero")
    auxiliares = relationship("AuxiliarDB", back_populates="enfermero")

class HabitacionDB(Base):
    __tablename__ = 'habitaciones'
    numero_habitacion = Column(Integer, primary_key=True)
    capacidad = Column(Integer)
    limpia = Column(Integer)  # 0 para sucia, 1 para limpia

    pacientes = relationship("PacienteDB", back_populates="habitacion")

class AuxiliarDB(Base):
    __tablename__ = 'auxiliares'
    id = Column(String, primary_key=True, unique=True)
    antiguedad = Column(Integer)
    id_enfermero = Column(String, ForeignKey('enfermeros.id'))

    enfermero = relationship("EnfermeroDB", back_populates="auxiliares")

class SipDB(Base):
    __tablename__ = 'sips'
    sip = Column(String, primary_key=True)
    paciente_id = Column(String, ForeignKey('pacientes.id'), unique=True, nullable=False)

    paciente = relationship("PacienteDB", back_populates="sip")

class CitaDB(Base):
    __tablename__ = 'citas'
    id_cita = Column(String, primary_key=True)
    paciente_id = Column(String, ForeignKey('pacientes.id'), nullable=False)
    medico_asignado = Column(String, ForeignKey('medicos.id'))
    fecha_hora = Column(String)
    tipo_cita = Column(String)
    motivo = Column(String)
    # Campos específicos para cada tipo de cita (podrían ser en tablas separadas para más normalización)
    centro = Column(String)
    telefono_contacto = Column(String)
    nivel_prioridad = Column(String)

    paciente = relationship("PacienteDB", back_populates="citas")
    medico = relationship("MedicoDB", back_populates="citas")
