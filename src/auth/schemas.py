from typing import Optional, List

from fastapi_users import schemas
from pydantic import EmailStr, Field, field_validator

from src.players.schemas import PlayerRead


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    # players: List[PlayerRead] = []

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str = Field(min_length=8)
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        password_length = len(value)
        if password_length < 8:
            raise ValueError("The password must be longer than 8 characters")
        return value


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is None:
            return

        password_length = len(value)
        if password_length < 8:
            raise ValueError("The password must be longer than 8 characters")
        return value


class UserUpdateSafe(schemas.BaseUserUpdate):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
