from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlmodel import Session
from app.db.database import get_session
from app.crud.user import get_user, get_users, create_user, update_user, delete_user
from app.auxiliares.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
def read_users(id: Optional[int] = Query(None), username: Optional[str] = None, email: Optional[str] = None,
               skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    if id:
        user = get_user(session, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return [user]
    return get_users(session, skip, limit)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: User, session: Session = Depends(get_session)):
    return create_user(session, user)

@router.put("/{user_id}", response_model=User)
def modify_user(user_id: int, user: User, session: Session = Depends(get_session)):
    updated = update_user(session, user_id, **user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, session: Session = Depends(get_session)):
    if not delete_user(session, user_id):
        raise HTTPException(status_code=404, detail="User not found")