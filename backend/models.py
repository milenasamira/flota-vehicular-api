# backend/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# --- CLASES BASE (Para Peticiones/Respuestas) ---
# Usadas por FastAPI/Pydantic para validar los datos que entran y salen.

class UsuarioBase(SQLModel):
    nombre: str
    email: str = Field(unique=True)
    rol: str = Field(default="usuario", description="usuario o administrador")

class VehiculoBase(SQLModel):
    marca: str
    modelo: str
    anio: int
    dominio: str = Field(unique=True, description="Matrícula/patente")
    estado: str = Field(default="disponible", description="disponible, en uso, mantenimiento")

class ReporteBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.utcnow)
    detalle: Optional[str] = None

# backend/models.py

# ... (tus imports arriba siguen igual)

# Modificamos esta clase para tener los 8 puntos de chequeo (Req 8)
class MantenimientoBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.utcnow)
    tipo: str = Field(default="VTV Anual")
    
    # Los 8 Puntos de Chequeo (Req 6: Puntuación de 1 a 10)
    luces: int = Field(default=10, ge=1, le=10)
    frenos: int = Field(default=10, ge=1, le=10)
    neumaticos: int = Field(default=10, ge=1, le=10)
    suspension: int = Field(default=10, ge=1, le=10)
    chasis: int = Field(default=10, ge=1, le=10)
    gases: int = Field(default=10, ge=1, le=10)
    direccion: int = Field(default=10, ge=1, le=10)
    seguridad: int = Field(default=10, ge=1, le=10)
    
    resultado_final: Optional[str] = None # Para guardar si fue APTO o RECHEQUEAR
    notas: Optional[str] = None # Para las observaciones del inspector
    
# --- CLASES TABLA (Para la Base de Datos) ---

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str 

    vehiculos: List["Vehiculo"] = Relationship(back_populates="propietario")

class Vehiculo(VehiculoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    propietario_id: int = Field(foreign_key="usuario.id")

    propietario: Usuario = Relationship(back_populates="vehiculos")
    reportes: List["Reporte"] = Relationship(back_populates="vehiculo")
    mantenimientos: List["Mantenimiento"] = Relationship(back_populates="vehiculo")

class Reporte(ReporteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehiculo_id: int = Field(foreign_key="vehiculo.id")
    usuario_id: int = Field(foreign_key="usuario.id")

    vehiculo: Vehiculo = Relationship(back_populates="reportes")

class Mantenimiento(MantenimientoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehiculo_id: int = Field(foreign_key="vehiculo.id")

    vehiculo: Vehiculo = Relationship(back_populates="mantenimientos")