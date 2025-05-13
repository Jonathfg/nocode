from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlmodel import Session
from app.db.database import get_session
from app.crud.task import get_task, get_tasks, create_task, update_task, delete_task
from app.auxiliares.models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 100, todo_list_id: Optional[int] = None,
               is_completed: Optional[bool] = None,
               session: Session = Depends(get_session)):
    all_tasks = get_tasks(session, skip, limit)
    if todo_list_id is not None:
        all_tasks = [t for t in all_tasks if t.todo_list_id == todo_list_id]
    if is_completed is not None:
        all_tasks = [t for t in all_tasks if t.is_completed == is_completed]
    return all_tasks

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(task: Task, session: Session = Depends(get_session)):
    return create_task(session, task)

@router.put("/{task_id}", response_model=Task)
def modify_task(task_id: int, task: Task, session: Session = Depends(get_session)):
    updated = update_task(session, task_id, **task.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int, session: Session = Depends(get_session)):
    if not delete_task(session, task_id):
        raise HTTPException(status_code=404, detail="Task not found")