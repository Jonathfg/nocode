from sqlmodel import Session, select
from app.auxiliares.models.user import User
from typing import List, Optional

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return session.exec(select(User).offset(skip).limit(limit)).all()

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, **kwargs) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
