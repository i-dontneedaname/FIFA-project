from typing import List

from fastapi import APIRouter, Depends

from src.auth.dependencies import current_active_user, current_superuser, get_user_or_404
from src.auth.models import User
from src.auth.schemas import UserRead, UserUpdate
from src.dependencies import ServiceManagerDep, Paginator
from src.auth.service import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserRead)
async def me(
        user: User = Depends(current_active_user)
):
    return user


@router.patch("/me", response_model=UserRead)
async def update_me(
        service_manager: ServiceManagerDep,
        update_fields: UserUpdate,
        user: User = Depends(current_active_user),
):
    update_fields_dict = update_fields.model_dump()

    if not user.is_superuser:
        update_fields_dict.pop('is_active')
        update_fields_dict.pop('is_superuser')
        update_fields_dict.pop('is_verified')

    updated_user = await UsersService().edit_user(service_manager, UserRead, user.id, update_fields_dict)
    return updated_user


@router.get("", response_model=List[UserRead])
async def get_users(
        service_manager: ServiceManagerDep,
        username: str = None,
        pagination: Paginator = Depends(Paginator)
):
    users_list = await UsersService().get_users(service_manager, UserRead, username, pagination)
    return users_list


@router.get("/{id}", response_model=UserRead)
async def get_user(
        service_manager: ServiceManagerDep,
        user=Depends(get_user_or_404)
):
    return user


@router.patch("/{id}", response_model=UserRead)
async def update_user(
        service_manager: ServiceManagerDep,
        update_fields: UserUpdate,
        updating_user=Depends(get_user_or_404),
        user: User = Depends(current_superuser),
):
    update_fields_dict = update_fields.model_dump()

    updated_user = await UsersService().edit_user(service_manager, UserRead, updating_user.id, update_fields_dict)
    return updated_user


@router.delete("/{id}")
async def delete_user(
        service_manager: ServiceManagerDep,
        deleting_user=Depends(get_user_or_404),
        user: User = Depends(current_superuser),
):
    deleted_user_id = await UsersService().delete_user(service_manager, deleting_user.id)
    return {"id": deleted_user_id}
