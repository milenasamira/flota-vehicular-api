
# Trabajo Final: Sistema de Gestión de Flota 

Aplicación web para gestionar turnos e inspecciones vehiculares. El sistema permite agendar vehículos, loguearse como inspector y cargar los resultados de la VTV (con validación automática de puntajes).

##  Tecnologías

  * **Backend:** Python (FastAPI) + SQLModel.
  * **Base de Datos:** PostgreSQL (corriendo en Docker).
  * **Frontend:** React + Vite.
  * **Tests:** Pytest.

-----

## Cómo levantar el proyecto

Requisito: Tener **Docker Desktop** abierto.

### 1\. Levantar la Base de Datos

Abrir una terminal en la carpeta raíz y ejecutar:

```bash
docker-compose up -d
```

### 2\. Iniciar el Backend

En una terminal, ir a la carpeta `backend`, activar el entorno y correr el servidor:

```bash
# Windows
cd backend
.\venv\Scripts\activate
cd ..
uvicorn backend.main:app --reload
```

*El backend queda corriendo en: `http://127.0.0.1:8000`*
*(Documentación automática en: `http://127.0.0.1:8000/docs`)*

### 3\. Iniciar el Frontend

Abrir **otra terminal nueva**, ir a la carpeta `frontend` y usar Docker para levantar React (así evitamos problemas de versiones de Node en Windows):

```bash
cd frontend
docker run -it --rm -p 5174:5173 -v ${PWD}:/app -w /app node:24-alpine npm run dev
```

*El frontend queda accesible en: `http://localhost:5174`*

-----

##  Detalles de la Implementación

### Arquitectura (No Monolítica)

Separé el proyecto en dos: el Backend (API) y el Frontend (Cliente) funcionan independiente. [cite\_start]El front solo consume los JSON que manda el back[cite: 6, 7].

### Patrones de Diseño

En el backend usé **Inyección de Dependencias** para no acoplar la lógica.

  * `api_vehiculos.py`: Solo maneja las rutas.
  * `servicios.py`: Tiene la lógica "fuerte" (validaciones, cálculos).
  * [cite\_start]`models.py`: Define cómo son las tablas[cite: 33, 34].

### Lógica de Negocio (VTV)

Implementé la validación de los **8 puntos de chequeo** (luces, frenos, etc.).

  * Si algún punto tiene menos de 5 -\> **Rechazado (Falla Grave)**.
  * Si la suma total es menor a 40 -\> **Rechazado**.
  * Si da más de 80 -\> **Apto**.

### Seguridad

Los endpoints críticos (como cargar una inspección) están protegidos. Hay que loguearse para conseguir un Token.

  * **Usuario para probar:** `admin`
  * **Password:** `admin`

### Tests

[cite\_start]Hice tests unitarios con **Pytest** usando Mocks para probar la lógica sin necesidad de que la base de datos real esté conectada[cite: 156, 208]. Para correrlos:

```bash
pytest
```

-----

