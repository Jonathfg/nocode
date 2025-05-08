from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

# Carga las variables del entorno
load_dotenv()

# Construcción de la URL de la base de datos desde .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Motor de conexión a PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from app.auxiliares.models import user, todo_list, task, task_status
    SQLModel.metadata.create_all(engine)

# Si quieres añadir datos iniciales, puedes crear una función aquí:
# def insert_sample_data(): ...
