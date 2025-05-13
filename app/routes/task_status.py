from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from app.db.database import get_session
from app.crud.task_status import get_status, get_statuses, create_status, update_status, delete_status
from app.auxiliares.models.task_status import TaskStatus

router = APIRouter(prefix="/status", tags=["status"])

@router.get("/", response_model=List[TaskStatus])
def read_statuses(session: Session = Depends(get_session)):
    return get_statuses(session)

@router.post("/", response_model=TaskStatus, status_code=status.HTTP_201_CREATED)
def create_new_status(status: TaskStatus, session: Session = Depends(get_session)):
    return create_status(session, status)

@router.put("/{status_id}", response_model=TaskStatus)
def modify_status(status_id: int, status: TaskStatus, session: Session = Depends(get_session)):
    updated = update_status(session, status_id, **status.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Status not found")
    return updated

@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_status(status_id: int, session: Session = Depends(get_session)):
    if not delete_status(session, status_id):
        raise HTTPException(status_code=404, detail="Status not found")
