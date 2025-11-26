# backend/api_vehiculos.py
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # <--- IMPORTANTE
from typing import List
from sqlmodel import Session

from backend.database import get_session
from backend.servicios import RepositorioVehiculos, ServicioMantenimiento
from backend.models import Vehiculo, VehiculoBase, Mantenimiento, MantenimientoBase, Usuario

# --- SEGURIDAD AUTOMÁTICA (Formulario) ---
# Esto hace que Swagger muestre la ventanita de "Username" y "Password"
# y llame automáticamente a tu endpoint /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

# --- Inyección de Dependencias ---
def get_vehiculo_repo(db: Session = Depends(get_session)) -> RepositorioVehiculos:
    return RepositorioVehiculos(db)

def get_mantenimiento_service(db: Session = Depends(get_session)) -> ServicioMantenimiento:
    return ServicioMantenimiento(db)

# --- Router ---
router = APIRouter(prefix="/api/v1", tags=["Sistema de Inspección VTV"])

# 1. Listar Slots
@router.get("/turnos/disponibles", response_model=List[Vehiculo])
def listar_turnos_disponibles(repo: RepositorioVehiculos = Depends(get_vehiculo_repo)):
    """1. Listar los slots para booking"""
    return repo.obtener_todos()

# 2. Agendar turno
@router.post("/turnos/agendar", response_model=Vehiculo, status_code=status.HTTP_201_CREATED)
def agendar_turno(
    vehiculo: VehiculoBase, 
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo)
):
    """2. Agendar un turno"""
    # Parche: Crear usuario 1 si no existe para que no falle
    usuario_default = repo.db.get(Usuario, 1)
    if not usuario_default:
        nuevo_usuario = Usuario(id=1, nombre="Demo", email="demo@test.com", password_hash="123")
        repo.db.add(nuevo_usuario)
        repo.db.commit()
        
    return repo.guardar_vehiculo(vehiculo, propietario_id=1)

# 3. Login (Adaptado para recibir datos del formulario de Swagger)
@router.post("/token")
def login_inspector(form_data: OAuth2PasswordRequestForm = Depends()): # <--- Recibe user/pass
    """3. Login con el inspector (Devuelve token al sistema)"""
    # ACÁ PODRÍAS VALIDAR: if form_data.username == "admin"...
    # Pero para la demo devolvemos siempre éxito:
    return {"access_token": "soy-un-token-falso-jwt", "token_type": "bearer"}

# 4 y 5. Crear Inspección (Privado - Requiere Login previo)
# backend/api_vehiculos.py (Dentro de la función crear_inspeccion)

@router.post("/inspecciones", response_model=Mantenimiento)
def crear_inspeccion(
    vehiculo_id: int,
    datos: MantenimientoBase, # Usamos 'datos' en lugar de 'servicio_data' para ser más claros
    token: str = Depends(obtener_usuario_actual),
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo),
    servicio: ServicioMantenimiento = Depends(get_mantenimiento_service)
):
    """4 y 5. Crear inspección y validar puntajes (Reglas VTV)"""
    repo.buscar_por_id(vehiculo_id) 
    
    # --- LÓGICA DE NEGOCIO VTV (Req 7) ---
    
    # 1. Sumar los 8 puntos
    total_puntos = (
        datos.luces + datos.frenos + datos.neumaticos + datos.suspension +
        datos.chasis + datos.gases + datos.direccion + datos.seguridad
    )
    
    # 2. Verificar si algún punto individual es menor a 5 (Falla directa)
    hay_falla_grave = (
        datos.luces < 5 or datos.frenos < 5 or datos.neumaticos < 5 or 
        datos.suspension < 5 or datos.chasis < 5 or datos.gases < 5 or 
        datos.direccion < 5 or datos.seguridad < 5
    )

    # 3. Aplicar Reglas de Aprobación
    estado_vehiculo = "APTO" # Asumimos éxito y buscamos razones para fallar
    razon = ""

    if hay_falla_grave:
        estado_vehiculo = "RECHEQUEAR (Falla Grave)"
        razon = "Se detectó un componente con menos de 5 puntos."
        
    elif total_puntos < 40:
        estado_vehiculo = "RECHEQUEAR (Puntaje Bajo)"
        razon = f"El puntaje total ({total_puntos}) es menor a 40."
        
    elif total_puntos >= 80:
        estado_vehiculo = "APTO (Seguro)"
        razon = "Vehículo en condiciones óptimas."
    else:
        # Caso intermedio (entre 40 y 79)
        estado_vehiculo = "CONDICIONAL"
        razon = f"Puntaje regular ({total_puntos}). Requiere reparaciones menores."

    # Guardamos el resultado calculado
    datos.resultado_final = estado_vehiculo
    # Agregamos la razón automática a las notas del inspector
    datos.notas = f"[{estado_vehiculo}] {razon} - Observaciones: {datos.notas or ''}"

    return servicio.registrar_servicio(vehiculo_id, datos)

# 7. Obtener Reporte
@router.get("/reportes/{vehiculo_id}", response_model=List[Mantenimiento])
def obtener_reporte(
    vehiculo_id: int,
    repo: RepositorioVehiculos = Depends(get_vehiculo_repo),
    servicio: ServicioMantenimiento = Depends(get_mantenimiento_service)
):
    """7. Obtener el reporte"""
    repo.buscar_por_id(vehiculo_id)
    return servicio.listar_servicios_por_vehiculo(vehiculo_id)