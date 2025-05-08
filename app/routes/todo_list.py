from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_lists():
    return {"message": "Listado de listas de tareas"}
