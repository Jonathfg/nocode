from enum import Enum
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

class Role(str, Enum):
    admin  = "admin"
    user   = "user"
    viewer = "viewer"

if TYPE_CHECKING:
    from .todo_list import TodoList

class User(SQLModel, table=True):
    id: Optional[int]       = Field(default=None, primary_key=True)
    username: str           = Field(index=True, unique=True)
    email:    str           = Field(index=True, unique=True)
    hashed_password: str
    role: Role              = Field(default=Role.user, sa_column_kwargs={"server_default": Role.user.value})
    created_at: datetime    = Field(default_factory=datetime.utcnow)

    # Relación a listas
    lists: List["TodoList"] = Relationship(back_populates="owner")