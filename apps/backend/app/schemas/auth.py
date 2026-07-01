from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str | None = None


class CurrentUserResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)