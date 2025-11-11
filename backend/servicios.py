# backend/servicios.py

from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException, status

# Importa los modelos que acabamos de definir
from backend.models import Vehiculo, VehiculoBase, Mantenimiento, MantenimientoBase

# --- RepositorioVehiculos (Capa de Acceso a Datos - CRUD) ---
# ESTA es la clase que tu API no puede encontrar
class RepositorioVehiculos:
    
    def __init__(self, db: Session):
        self.db = db

    def guardar_vehiculo(self, vehiculo_data: VehiculoBase, propietario_id: int) -> Vehiculo:
        db_vehiculo = Vehiculo.model_validate(vehiculo_data, update={'propietario_id': propietario_id})
        self.db.add(db_vehiculo)
        self.db.commit()
        self.db.refresh(db_vehiculo)
        return db_vehiculo

    def obtener_todos(self) -> List[Vehiculo]:
        statement = select(Vehiculo)
        return self.db.exec(statement).all()

    def buscar_por_id(self, vehiculo_id: int) -> Vehiculo:
        vehiculo = self.db.get(Vehiculo, vehiculo_id)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehiculo
    
    def actualizar_estado(self, vehiculo_id: int, nuevo_estado: str) -> Vehiculo:
        vehiculo = self.buscar_por_id(vehiculo_id)
        
        estados_validos = ["disponible", "en uso", "mantenimiento"]
        if nuevo_estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Estado inválido. Debe ser uno de {estados_validos}"
            )

        vehiculo.estado = nuevo_estado
        self.db.add(vehiculo)
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

# --- ServicioMantenimiento (Lógica de Negocio específica) ---
# ESTA es la otra clase que faltaba
class ServicioMantenimiento:

    def __init__(self, db: Session):
        self.db = db

    def registrar_servicio(self, vehiculo_id: int, servicio_data: MantenimientoBase) -> Mantenimiento:
        db_mantenimiento = Mantenimiento.model_validate(servicio_data, update={'vehiculo_id': vehiculo_id})
        self.db.add(db_mantenimiento)
        self.db.commit()
        self.db.refresh(db_mantenimiento)
        return db_mantenimiento

    def listar_servicios_por_vehiculo(self, vehiculo_id: int) -> List[Mantenimiento]:
        statement = select(Mantenimiento).where(Mantenimiento.vehiculo_id == vehiculo_id)
        return self.db.exec(statement).all()