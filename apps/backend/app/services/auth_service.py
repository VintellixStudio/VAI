from app.core.security import get_password_hash


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return get_password_hash(password)