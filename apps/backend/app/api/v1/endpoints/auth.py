from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from fastapi import Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import CurrentUserResponse

router = APIRouter()

@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Get current authenticated user",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get(
    "/me",
    response_model=UserRead,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = UserService(repository)

    if repository.get_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if repository.get_by_username(payload.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    return service.create_user(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        return service.login(
            payload.email,
            payload.password,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )