from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_statuses():
    return {"message": "Listado de estados de tarea"}