from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            hashed_password=get_password_hash(data.password),
            is_active=True,
            is_superuser=False,
        )
        return self.repository.create(user)

    def get_users(self) -> list[User]:
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def update_user(self, user_id: int, data: UserUpdate) -> User | None:
        user = self.repository.get_by_id(user_id)

        if not user:
            return None

        if data.username is not None:
            user.username = data.username

        if data.email is not None:
            user.email = data.email

        if data.full_name is not None:
            user.full_name = data.full_name

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.repository.get_by_id(user_id)

        if not user:
            return False

        self.repository.delete(user)
        return True