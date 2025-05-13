from app.db.database import engine, get_session
from app.db.database import engine, create_db_and_tables as init_db
from app.auxiliares.models.user import User
from app.auxiliares.models.todo_list import TodoList
from app.auxiliares.models.task_status import TaskStatus
from app.auxiliares.models.task import Task
from sqlmodel import Session

def seed():
    init_db()
    with Session(engine) as session:
        # Estados
        pend = TaskStatus(name="Pendiente", color="red")
        prog = TaskStatus(name="En progreso", color="yellow")
        comp = TaskStatus(name="Completada", color="green")
        session.add_all([pend, prog, comp])
        session.commit()

        # Usuario
        u = User(username="johndoe", email="johndoe@example.com", hashed_password="hashed123")
        session.add(u)
        session.commit()
        session.refresh(u)

        # Lista
        lst = TodoList(title="Trabajo", description="Tareas de trabajo", owner_id=u.id)
        session.add(lst)
        session.commit()
        session.refresh(lst)

        # Tareas
        t1 = Task(title="Comprar material", todo_list_id=lst.id, status_id=pend.id)
        t2 = Task(title="Reunión equipo", todo_list_id=lst.id, status_id=prog.id)
        session.add_all([t1, t2])
        session.commit()
    print("Seeding completed.")

if __name__ == "__main__":
    seed()