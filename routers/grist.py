from fastapi import APIRouter

from services import update_grist_service

router = APIRouter()


@router.post("/grist")
def update_grist():
    update_grist_service()
