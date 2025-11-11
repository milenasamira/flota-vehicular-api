# Sistema de Gestión de Flota de Vehículos (Cliente-Servidor)

Este proyecto implementa una solución no monolítica para el control de flota, desarrollada con Python y JavaScript, y verificada con tests unitarios

## 1\. Guía de Despliegue

### Requisitos Previos

Necesita tener Docker Desktop, Python 3.11 (con el `venv` activado), y Node.js (se utilizará a través de Docker).

### Paso 1: Iniciar la Base de Datos (PostgreSQL en Docker)

Inicie el contenedor de PostgreSQL en el puerto 5433 desde la raíz del proyecto (`fleet-management-app`):

```bash
docker-compose up -d
```

### Paso 2: Iniciar el Backend (FastAPI API)
El Backend, desarrollado en Python/FastAPI , se inicia y automáticamente crea las tablas SQL (usuarios, vehículos, etc.)

1.  Active el `venv` y regrese a la raíz.
2.  Ejecute el servidor API (Terminal 1):
    ```bash
    (venv) uvicorn backend.main:app --reload
    ```
    (API URL: `http://127.0.0.1:8000`)

### Paso 3: Iniciar el Frontend (React Cliente)

Abra una segunda terminal. El Frontend, desarrollado en React , consume la API REST del Backend.
1.  Navegue a la carpeta `frontend`: `cd frontend`
2.  Ejecute el servidor React (Terminal 2), usando Docker para evitar problemas de NPM:
    ```bash
    docker run -it --rm -p 5174:5173 -v ${PWD}:/app -w /app node:24-alpine npm run dev
    ```
    (Frontend URL: `http://localhost:5174`)

-----

## 2\. Justificación de Arquitectura y Conceptos

### 2.1. Arquitectura y Orientación a Servicios

La solución es **no monolítica** (orientada a servicios)[cite: 10]. El Backend (FastAPI) y el Frontend (React) son servidores independientes que se comunican mediante una API REST. Esta separación permite un bajo acoplamiento y futuras mejoras sin afectar la lógica de negocio.

### 2.2. POO y Inyección de Dependencias (DI)

El Backend implementa Programación Orientada a Objetos y utiliza el patrón de **Inyección de Dependencias (DI)**. Esto se hace para separar el acceso a datos (Repositorios) de la lógica de negocio (Servicios), asegurando una alta cohesión y bajo acoplamiento.

### 2.3. Pruebas Unitarias

Se utilizó **Pytest** para la verificación. Las pruebas unitarias se enfocaron en la capa de Servicios/Repositorios, usando *mocks* para simular la base de datos. Esto confirma que la lógica crítica (ej. `actualizar_estado`) es correcta y que el diseño con DI es exitos.
