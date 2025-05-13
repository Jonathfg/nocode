import logging.config
from fastapi import FastAPI, Request
from app.db.database import create_db_and_tables
from app.routes import user, todo_list, task_status, task
import os

# Logging
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task Manager API")

# Iniciar base de datos
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("Database initialized")

# Middleware para loggear cada petición
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"--> {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"<-- {request.method} {request.url.path} - {response.status_code}")
    return response

# Routers
app.include_router(user.router)
app.include_router(todo_list.router)
app.include_router(task_status.router)
app.include_router(task.router)