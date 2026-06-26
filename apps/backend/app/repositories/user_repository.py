from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    def get_by_id(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )
        