# backend/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Usamos importaciones absolutas para evitar errores
from backend.database import create_db_and_tables
from backend.api_vehiculos import router as vehiculo_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando API y creando tablas de base de datos...")
    create_db_and_tables() 
    yield

app = FastAPI(title="Fleet Management API", lifespan=lifespan)

# Conectar el router de la API
app.include_router(vehiculo_router)

@app.get("/")
def read_root():
    return {"message": "Fleet Management API funcionando"}