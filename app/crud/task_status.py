from sqlmodel import Session, select
from app.auxiliares.models.task_status import TaskStatus
from typing import List, Optional

def get_status(session: Session, status_id: int) -> Optional[TaskStatus]:
    return session.get(TaskStatus, status_id)

def get_statuses(session: Session) -> List[TaskStatus]:
    return session.exec(select(TaskStatus)).all()

def create_status(session: Session, status: TaskStatus) -> TaskStatus:
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def update_status(session: Session, status_id: int, **kwargs) -> Optional[TaskStatus]:
    status = session.get(TaskStatus, status_id)
    if not status:
        return None
    for key, value in kwargs.items():
        setattr(status, key, value)
    session.add(status)
    session.commit()
    session.refresh(status)
    return status

def delete_status(session: Session, status_id: int) -> bool:
    status = session.get(TaskStatus, status_id)
    if not status:
        return False
    session.delete(status)
    session.commit()
    return True
