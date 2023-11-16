from typing import Optional

from pydantic import BaseModel


class PlayerStatisticRead(BaseModel):
    matches: int
    win_rate: float
    total_goals: int
    avg_goals: float
    avg_xg: float
    avg_ball_possession: float
    avg_strikes: float
    avg_yellow_cards: float
    avg_red_cards: float

    class Config:
        from_attributes = True


class PlayerRead(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class PlayerReadWithStatistic(PlayerRead):
    statistic: Optional[PlayerStatisticRead] = {}


class PlayerCreate(BaseModel):
    name: str
