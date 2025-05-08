from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.routes import user, todo_list, task, task_status

app = FastAPI(
    title="Todo List API",
    description="API para gestión de tareas con usuarios, listas y estados.",
    version="1.0.0"
)

# Inicializa la base de datos
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Rutas
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(todo_list.router, prefix="/lists", tags=["Todo Lists"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(task_status.router, prefix="/status", tags=["Task Status"])

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de tareas"}
