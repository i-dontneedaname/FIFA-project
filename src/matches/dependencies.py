from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.dependencies import ServiceManagerDep
from src.matches.schemas import MatchRead
from src.matches.service import MatchesService


async def get_match_or_404(
        service_manager: ServiceManagerDep,
        id: int
):
    try:
        match = await MatchesService().get_match(service_manager, MatchRead, id)
        return match
    except (NoResultFound, IndexError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
