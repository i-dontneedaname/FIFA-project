from abc import ABC, abstractmethod
from typing import Type

from src.database import async_session_maker
from src.auth.repository import UsersRepository
from src.matches.repository import MatchesRepository
from src.players.repository import PlayersRepository


class IServiceManager(ABC):
    users: Type[UsersRepository]
    players: Type[PlayersRepository]
    matches: Type[MatchesRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class ServiceManager:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.players = PlayersRepository(self.session)
        self.matches = MatchesRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

