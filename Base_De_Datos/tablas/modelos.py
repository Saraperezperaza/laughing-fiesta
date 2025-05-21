from sqlalchemy import Column, Integer, String, ForeignKey
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

class MedicoDB(Base):
    __tablename__ = 'medicos'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    especialidad = Column(String)
    antiguedad = Column(Integer)

class EnfermeroDB(Base):
    __tablename__ = 'enfermeros'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    antieguedad = Column(Integer)
    especialidad = Column(String)
