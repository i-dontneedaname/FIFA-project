from src.players.models import Player
from src.utils.repository import SQLAlchemyRepository


class PlayersRepository(SQLAlchemyRepository):
    model = Player

    # async def get_player_statistic(self):
    #     pass
    #
    # async def find_one(self):
    #     pass
