# backend/api_vehiculos.py
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

# Importaciones ABSOLUTAS para asegurar que Python las encuentre
from backend.database import get_session
from backend.servicios import RepositorioVehiculos, ServicioMantenimiento
from backend.models import Vehiculo, VehiculoBase, Mantenimiento, MantenimientoBase

# --- Inyección de Dependencias (DI) ---

def get_vehiculo_repo(db: Session = Depends(get_session)) -> RepositorioVehiculos:
    return RepositorioVehiculos(db)

def get_mantenimiento_service(db: Session = Depends(get_session)) -> ServicioMantenimiento:
    return ServicioMantenimiento(db)

# --- API Router (Controlador) ---
# ESTA es la variable 'router' que main.py está buscando.
router = APIRouter(prefix="/api/vehiculos", tags=["Vehículos y Mantenimiento"])

@router.post("/", response_model=Vehiculo, status_code=status.HTTP_201_CREATED)
def agregar_vehiculo(
    vehiculo: VehiculoBase, 
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo)
):
    # Asumimos propietario_id = 1 temporalmente (sin auth)
    return repo.guardar_vehiculo(vehiculo, propietario_id=1) 

@router.get("/", response_model=List[Vehiculo])
def listar_vehiculos(repo: RepositorioVehiculos = Depends(get_vehiculo_repo)):
    return repo.obtener_todos()

@router.patch("/{vehiculo_id}/estado", response_model=Vehiculo)
def actualizar_estado(
    vehiculo_id: int, 
    nuevo_estado: str,
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo)
):
    return repo.actualizar_estado(vehiculo_id, nuevo_estado)

@router.post("/{vehiculo_id}/mantenimientos", response_model=Mantenimiento, status_code=status.HTTP_201_CREATED)
def registrar_mantenimiento(
    vehiculo_id: int,
    servicio_data: MantenimientoBase,
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo),
    servicio: ServicioMantenimiento = Depends(get_mantenimiento_service)
):
    repo.buscar_por_id(vehiculo_id) 
    return servicio.registrar_servicio(vehiculo_id, servicio_data)

@router.get("/{vehiculo_id}/mantenimientos", response_model=List[Mantenimiento])
def historial_mantenimientos(
    vehiculo_id: int,
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo),
    servicio: ServicioMantenimiento = Depends(get_mantenimiento_service)
):
    repo.buscar_por_id(vehiculo_id)
    return servicio.listar_servicios_por_vehiculo(vehiculo_id)