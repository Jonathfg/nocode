# app/crud/user.py
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.auxiliares.models.user import User, Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return session.exec(select(User).offset(skip).limit(limit)).all()

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.exec(
        select(User).where(User.username == username)
    ).first()

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(
        select(User).where(User.email == email)
    ).first()

def create_user(
    session: Session,
    username: str,
    email: str,
    password: str,
    role: Role = Role.user
) -> Optional[User]:
    hashed = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=hashed, role=role)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, **kwargs) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    # Si traen password, rehashearlo
    if "password" in kwargs:
        user.hashed_password = get_password_hash(kwargs.pop("password"))
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