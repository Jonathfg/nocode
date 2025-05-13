# nocode
Desarrollo de una API RESTful para un sistema de gestión de tareas


# Task Manager API

Sistema de gestión de tareas implementado con FastAPI, SQLModel y PostgreSQL.

## Instalación

1. Clona el repositorio.
2. Crea y activa un virtualenv.
3. Copia `.env.example` a `.env` y ajusta `DATABASE_URL`.
4. `pip install -r requirements.txt`
5. Ejecuta `python seeder.py`
6. Levanta el servidor: `uvicorn app.main:app --reload`

## Endpoints

- **Usuarios**: `/users`
- **Listas**: `/lists`
- **Tareas**: `/tasks`
- **Estados**: `/status`

Consulta el código en `app/routes` para más detalles.
