from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlmodel import Session
from app.db.database import get_session
from app.crud.todo_list import get_list, get_lists, create_list, update_list, delete_list
from app.auxiliares.models.todo_list import TodoList

router = APIRouter(prefix="/lists", tags=["lists"])

@router.get("/", response_model=List[TodoList])
def read_lists(id: Optional[int] = Query(None), owner_id: Optional[int] = None,
               skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    if id:
        lst = get_list(session, id)
        if not lst:
            raise HTTPException(status_code=404, detail="List not found")
        return [lst]
    return get_lists(session, skip, limit)

@router.post("/", response_model=TodoList, status_code=status.HTTP_201_CREATED)
def create_new_list(todo_list: TodoList, session: Session = Depends(get_session)):
    return create_list(session, todo_list)

@router.put("/{list_id}", response_model=TodoList)
def modify_list(list_id: int, todo_list: TodoList, session: Session = Depends(get_session)):
    updated = update_list(session, list_id, **todo_list.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="List not found")
    return updated

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_list(list_id: int, session: Session = Depends(get_session)):
    if not delete_list(session, list_id):
        raise HTTPException(status_code=404, detail="List not found")
