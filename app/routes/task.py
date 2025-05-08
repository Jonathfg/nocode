from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_tasks():
    return {"message": "Listado de tareas"}