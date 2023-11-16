from typing import List, Optional

from fastapi import APIRouter, Depends

from src.dependencies import ServiceManagerDep, Paginator
from src.auth.dependencies import current_active_user, current_superuser, get_user_or_404
from src.auth.models import User
from src.players.schemas import PlayerCreate, PlayerReadWithStatistic
from src.players.service import PlayersService
from src.players.dependencies import get_player_or_404

router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


@router.post("", response_model=PlayerReadWithStatistic)
async def add_player(
        service_manager: ServiceManagerDep,
        player: PlayerCreate,
        user: User = Depends(current_active_user)

):
    player_dict = player.model_dump()
    player_dict["owner_id"] = user.id

    added_player = await PlayersService().add_player(service_manager, PlayerReadWithStatistic, player_dict)
    return added_player


@router.get("", response_model=List[PlayerReadWithStatistic])
async def get_players(
        service_manager: ServiceManagerDep,
        pagination: Paginator = Depends(Paginator),
        owner_id: int = None
):
    players_list = await PlayersService().get_players(service_manager, PlayerReadWithStatistic, owner_id, pagination)
    return players_list


@router.get("/{id}", response_model=PlayerReadWithStatistic)
async def get_player(
        service_manager: ServiceManagerDep,
        player=Depends(get_player_or_404)
):
    return player


