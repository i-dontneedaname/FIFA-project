from typing import Optional

from src.utils.service_manager import IServiceManager


class PlayersService:

    async def add_player(
            self,
            service_manager: IServiceManager,
            response_schema,
            data: dict
    ):
        async with service_manager:
            player = await service_manager.players.add_one(data)
            await service_manager.commit()
            return response_schema.model_validate(player)

    async def get_players(
            self,
            service_manager: IServiceManager,
            response_schema,
            owner_id: int,
            pagination
    ):
        async with service_manager:
            if owner_id:
                players = await service_manager.players.find_all(pagination, owner_id=owner_id)
            else:
                players = await service_manager.players.find_all(pagination)
            return [response_schema.model_validate(row) for row in players]

    async def get_player(
            self,
            service_manager: IServiceManager,
            response_schema,
            id: int
    ):
        async with service_manager:
            player = await service_manager.players.find_one(id=id)
            return response_schema.model_validate(player)
