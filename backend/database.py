# backend/database.py

from sqlmodel import create_engine, SQLModel, Session
# Importa todos los modelos para que SQLModel sepa qué tablas crear
from .models import *
DATABASE_URL = "postgresql://user:password@localhost:5433/fleetdb" 

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=False) 

def create_db_and_tables():
    """Crea las tablas en PostgreSQL si no existen."""
    # SQLModel usa las clases de models.py para generar las sentencias CREATE TABLE
    SQLModel.metadata.create_all(engine) # <--- Esta es la función que debe existir

def get_session():
    """Generador para obtener una sesión de base de datos, usada por FastAPI Depends()."""
    with Session(engine) as session:
        yield session