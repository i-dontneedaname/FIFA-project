from typing import List

from fastapi import APIRouter, Depends

from src.auth.dependencies import current_active_user
from src.auth.models import User
from src.dependencies import ServiceManagerDep, Paginator
from src.matches.dependencies import get_match_or_404
from src.matches.schemas import MatchCreate, MatchRead
from src.matches.service import MatchesService

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.get("/{id}", response_model=MatchRead)
async def get_match(
        service_manager: ServiceManagerDep,
        match=Depends(get_match_or_404)
):
    return match


@router.get("/", response_model=List[MatchRead])
async def get_matches(
        service_manager: ServiceManagerDep,
        pagination: Paginator = Depends(Paginator)
):
    matches_list = await MatchesService().get_matches(service_manager, MatchRead, pagination)
    return matches_list


@router.post("", response_model=MatchRead)
async def add_match(
        service_manager: ServiceManagerDep,
        match: MatchCreate,
        user: User = Depends(current_active_user)
):
    match_dict = match.model_dump()
    match = await MatchesService().add_match(service_manager, MatchRead, match_dict, user.id)
    return match
