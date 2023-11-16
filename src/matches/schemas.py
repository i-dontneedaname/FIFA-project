from pydantic import BaseModel
from datetime import datetime

from src.players.schemas import PlayerRead


class MatchResult(BaseModel):
    player: PlayerRead
    victory: bool
    goals: int
    ball_possession: int
    strikes: int
    xg: float
    passes: int
    selections: int
    successful_selections: int
    interceptions: int
    saves: int
    violations: int
    offsides: int
    corners: int
    free_kicks: int
    penalty_kicks: int
    yellow_cards: int
    red_cards: int

    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    date: datetime
    minutes: str
    seconds: str
    first_team: MatchResult
    second_team: MatchResult


class MatchRead(BaseModel):
    id: int
    date: datetime
    minutes: str
    seconds: str
    first_team: MatchResult
    second_team: MatchResult

    class Config:
        from_attributes = True
