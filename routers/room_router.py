from fastapi import APIRouter
from managers.connection_manager import manager

router = APIRouter(prefix="/api/rooms")

@router.get("/")
def get_active_rooms():
    return manager.get_active_rooms()
