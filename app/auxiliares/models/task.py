# app/auxiliares/models/task.py
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .todo_list import TodoList
    from .task_status import TaskStatus

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool = Field(default=False)
    todo_list_id: int   = Field(foreign_key="todolist.id")
    status_id:    int   = Field(foreign_key="taskstatus.id")
    created_at:   datetime = Field(default_factory=datetime.utcnow)

    todo_list:    "TodoList"   = Relationship(back_populates="tasks")
    status:       "TaskStatus" = Relationship(back_populates="tasks")
