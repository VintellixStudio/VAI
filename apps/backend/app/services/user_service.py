from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)