from src.auth.utils import password_helper
from src.utils.helpers import delete_none_values_from_dict
from src.utils.service_manager import IServiceManager
from src.auth.schemas import UserUpdate


class UsersService:

    async def get_user(
            self,
            service_manager: IServiceManager,
            response_schema,
            id: int
    ):
        async with service_manager:
            user = await service_manager.users.find_one(id=id)
            return response_schema.model_validate(user)

    async def get_users(
            self,
            service_manager: IServiceManager,
            response_schema,
            username: str,
            pagination
    ):
        async with service_manager:
            users = await service_manager.users.find_all(pagination, username=username)
            return [response_schema.model_validate(row) for row in users]

    async def edit_user(
            self,
            service_manager: IServiceManager,
            response_schema,
            id: int,
            update_fields_dict: dict
    ):
        async with service_manager:
            update_fields_dict = delete_none_values_from_dict(update_fields_dict)

            if 'password' in update_fields_dict:
                password = update_fields_dict.pop('password')
                UserUpdate.validate_password(password)
                hashed_password = password_helper.hash(password)
                update_fields_dict['hashed_password'] = hashed_password

            updated_user = await service_manager.users.edit_one(id, update_fields_dict)
            await service_manager.commit()
            return response_schema.model_validate(updated_user)

    async def delete_user(
            self,
            service_manager: IServiceManager,
            id
    ):
        async with service_manager:
            deleted_user_id = await service_manager.users.delete_one(id)
            await service_manager.commit()
            return deleted_user_id
