from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.auth.base_config import fastapi_users
from src.dependencies import ServiceManagerDep
from src.auth.schemas import UserRead
from src.auth.service import UsersService

current_user = fastapi_users.current_user()

current_active_user = fastapi_users.current_user(active=True)

current_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_user_or_404(
        service_manager: ServiceManagerDep,
        id: int
):
    try:
        user = await UsersService().get_user(service_manager, UserRead, id)
        return user
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
