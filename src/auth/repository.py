from sqlalchemy import select, func, literal
from sqlalchemy.orm import joinedload

from src.auth.models import User
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    def add_one(self, data: dict) -> int:
        raise Exception()

    async def find_all(self, pagination=None, **filter_by):
        # stmt = select(self.model).options(joinedload(self.model.players))
        stmt = select(self.model)
        if filter_by['username']:
            stmt = stmt.filter(self.model.username.contains(filter_by['username']))
        if pagination is not None:
            if pagination.limit:
                stmt = stmt.limit(pagination.limit)
            if pagination.offset:
                stmt = stmt.offset(pagination.offset)
        res = await self.session.execute(stmt)
        # res = res.unique()
        return res.scalars().all()
