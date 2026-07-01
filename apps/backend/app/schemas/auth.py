from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserRead


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str | None = None


class CurrentUserResponse(UserRead):
    model_config = ConfigDict(from_attributes=True)