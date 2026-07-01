from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(data)


@router.get("/", response_model=list[UserResponse])
def get_users(
    service: UserService = Depends(get_user_service),
):
    return service.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = service.update_user(user_id, data)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    deleted = service.delete_user(user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")