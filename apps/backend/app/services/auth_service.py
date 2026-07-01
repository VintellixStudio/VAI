from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = self.repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    def login(
        self,
        email: str,
        password: str,
    ) -> dict:
        user = self.authenticate(
            email,
            password,
        )

        if not user:
            raise ValueError("Invalid credentials")

        return {
            "access_token": create_access_token(
                str(user.id),
            ),
            "refresh_token": create_refresh_token(
                str(user.id),
            ),
            "token_type": "bearer",
        }