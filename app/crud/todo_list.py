from sqlmodel import Session, select
from app.auxiliares.models.todo_list import TodoList
from typing import List, Optional

def get_list(session: Session, list_id: int) -> Optional[TodoList]:
    return session.get(TodoList, list_id)

def get_lists(session: Session, skip: int = 0, limit: int = 100) -> List[TodoList]:
    return session.exec(select(TodoList).offset(skip).limit(limit)).all()

def create_list(session: Session, todo_list: TodoList) -> TodoList:
    session.add(todo_list)
    session.commit()
    session.refresh(todo_list)
    return todo_list

def update_list(session: Session, list_id: int, **kwargs) -> Optional[TodoList]:
    todo_list = session.get(TodoList, list_id)
    if not todo_list:
        return None
    for key, value in kwargs.items():
        setattr(todo_list, key, value)
    session.add(todo_list)
    session.commit()
    session.refresh(todo_list)
    return todo_list

def delete_list(session: Session, list_id: int) -> bool:
    todo_list = session.get(TodoList, list_id)
    if not todo_list:
        return False
    session.delete(todo_list)
    session.commit()
    return True
