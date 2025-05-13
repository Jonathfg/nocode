# app/auxiliares/models/todo_list.py
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    # Estos imports *solo* se usan para mypy / IDE, no en tiempo de ejecución
    from .task import Task
    from .user import User

class TodoList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Referencias por cadena, no imports directos
    owner: Optional["User"] = Relationship(back_populates="lists")
    tasks: List["Task"]    = Relationship(back_populates="todo_list")
