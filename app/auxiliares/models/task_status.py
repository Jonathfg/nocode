from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from app.auxiliares.models.task import Task

class TaskStatus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    color: Optional[str] = None

    tasks: List["Task"] = Relationship(back_populates="status")
