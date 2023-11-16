from sqlalchemy import select
from sqlalchemy.orm import joinedload, Query, aliased
from src.matches.models import Match
from src.utils.repository import SQLAlchemyRepository


class MatchesRepository(SQLAlchemyRepository):
    model = Match

    async def find_all(self, pagination=None, **filter_by):
        stmt = select(self.model).filter_by(**filter_by).options(joinedload(self.model.player))

        if pagination is not None:
            if pagination.limit:
                stmt = stmt.limit(pagination.limit)
            if pagination.offset:
                stmt = stmt.offset(pagination.offset)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    # async def add_one(self, data: dict):
    async def get_last_match_id(self):
        stmt = select(self.model.id).order_by(self.model.id).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar_one()
