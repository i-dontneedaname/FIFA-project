from datetime import datetime
from sqlalchemy import String, ForeignKey, TIMESTAMP, Boolean, Integer, SmallInteger, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.players.models import Player


class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"), primary_key=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    victory: Mapped[bool] = mapped_column(Boolean, nullable=False)
    minutes: Mapped[str] = mapped_column(String(length=3), nullable=False)
    seconds: Mapped[str] = mapped_column(String(length=2), nullable=False)
    goals: Mapped[int] = mapped_column(SmallInteger)
    ball_possession: Mapped[int] = mapped_column(SmallInteger)
    strikes: Mapped[int] = mapped_column(SmallInteger)
    xg: Mapped[float] = mapped_column(Float(precision=1))
    passes: Mapped[int] = mapped_column(SmallInteger)
    selections: Mapped[int] = mapped_column(SmallInteger)
    successful_selections: Mapped[int] = mapped_column(SmallInteger)
    interceptions: Mapped[int] = mapped_column(SmallInteger)
    saves: Mapped[int] = mapped_column(SmallInteger)
    violations: Mapped[int] = mapped_column(SmallInteger)
    offsides: Mapped[int] = mapped_column(SmallInteger)
    corners: Mapped[int] = mapped_column(SmallInteger)
    free_kicks: Mapped[int] = mapped_column(SmallInteger)
    penalty_kicks: Mapped[int] = mapped_column(SmallInteger)
    yellow_cards: Mapped[int] = mapped_column(SmallInteger)
    red_cards: Mapped[int] = mapped_column(SmallInteger)

    player: Mapped['Player'] = relationship()

    # def to_read_model(self) -> UserRead:
    #     return UserRead(
    #         id=self.id,
    #         email=self.email,
    #         username=self.username,
    #         is_active=self.is_active,
    #         is_superuser=self.is_superuser,
    #         is_verified=self.is_verified
    #     )
