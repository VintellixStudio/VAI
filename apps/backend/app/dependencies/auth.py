from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_token, oauth2_scheme
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

    except (JWTError, ValueError):
        raise credentials_exception

    user = UserRepository(db).get_by_email(subject)

    if user is None:
        raise credentials_exception

    return user