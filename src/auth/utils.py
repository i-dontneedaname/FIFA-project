from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext

from src.auth.models import User
from src.database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_helper = PasswordHelper(context)
