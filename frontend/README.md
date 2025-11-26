

#Sistema de Gestión de Flota de Vehículos (Cliente-Servidor)
Este proyecto implementa una solución no monolítica para el control de flota, desarrollada con Python y JavaScript, y verificada con tests unitarios.

1. Guía de Despliegue
Requisitos Previos
Necesita tener Docker Desktop, Python 3.11 (con el venv activado), y Node.js (se utilizará a través de Docker).

Paso 1: Iniciar la Base de Datos (PostgreSQL en Docker)
Desde la raíz del proyecto (fleet-management-app):

Bash

docker-compose up -d
Paso 2: Iniciar el Backend (FastAPI API)
Active el venv y regrese a la raíz.

Ejecute el servidor API (Terminal 1):

Bash

(venv) uvicorn backend.main:app --reload
(API URL: http://127.0.0.1:8000)

Paso 3: Iniciar el Frontend (React Cliente)
Abra una segunda terminal. Navegue a la carpeta frontend y ejecute el servidor React (Terminal 2):

Bash

cd frontend
docker run -it --rm -p 5174:5173 -v ${PWD}:/app -w /app node:24-alpine npm run dev
(Frontend URL: http://localhost:5174)

2. Justificación de Arquitectura y Conceptos
Arquitectura y Orientación a Servicios
La solución es no monolítica (orientada a servicios). El Backend (FastAPI) y el Frontend (React) son servidores independientes que se comunican mediante una API REST.

POO y Inyección de Dependencias (DI)
El Backend utiliza POO, con separación de responsabilidades:

Repositorios manejan el CRUD y las transacciones.

Servicios contienen la lógica de negocio (ej. validación del estado del vehículo).

Se utiliza Inyección de Dependencias (DI) para conectar estas capas, lo que reduce el acoplamiento y facilita el testeo .

Pruebas Unitarias
Se utilizó Pytest para la verificación. Las pruebas unitarias se enfocaron en la capa de Servicios/Repositorios, usando mocks para simular la base de datos. Esto confirma que la lógica crítica (ej. actualizar_estado) es correcta y que el diseño con DI es exitoso.