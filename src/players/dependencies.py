from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.dependencies import ServiceManagerDep
from src.players.schemas import PlayerRead
from src.players.service import PlayersService


async def get_player_or_404(
        service_manager: ServiceManagerDep,
        id: int
):
    try:
        player = await PlayersService().get_player(service_manager, PlayerRead, id)
        return player
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
