from typing import List, TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.auth.schemas import UserRead

if TYPE_CHECKING:
    from src.players.models import Player


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )

    players: Mapped[List['Player']] = relationship(cascade='all, delete', back_populates="owner")

    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            email=self.email,
            username=self.username,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified
        )
