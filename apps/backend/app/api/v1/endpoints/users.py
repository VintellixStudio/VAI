from fastapi import APIRouter, Depends

from app.dependencies.user import get_user_service
from app.services.user_service import UserService

router = APIRouter()


@router.get("/")
def get_users(
    service: UserService = Depends(get_user_service),
):
    return {
        "message": "Users endpoint",
        "service": "connected",
    }