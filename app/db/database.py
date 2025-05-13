from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from app.auxiliares.models.user import User
    from app.auxiliares.models.todo_list import TodoList
    from app.auxiliares.models.task import Task
    from app.auxiliares.models.task_status import TaskStatus
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency para FastAPI: crea una sesión por petición y la cierra al terminar.
    """
    with Session(engine) as session:
        yield session
