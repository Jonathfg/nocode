from sqlmodel import Session, select
from app.auxiliares.models.task import Task
from typing import List, Optional

def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)

def get_tasks(session: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    return session.exec(select(Task).offset(skip).limit(limit)).all()

def create_task(session: Session, task: Task) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update_task(session: Session, task_id: int, **kwargs) -> Optional[Task]:
    task = session.get(Task, task_id)
    if not task:
        return None
    for key, value in kwargs.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
