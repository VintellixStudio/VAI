from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.security import oauth2_scheme
from app.core.settings import settings
from app.dependencies.database import DBSession
from app.models.user import User
from app.repositories.user_repository import UserRepository


def get_current_user(
    db: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        subject: str | None = payload.get("sub")

        if subject is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = UserRepository(db).get_by_email(subject)

    if user is None:
        raise credentials_exception

    return user