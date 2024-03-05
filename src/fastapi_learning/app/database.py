
from pathlib import Path

import dotenv
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

from fastapi_learning.app.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(BASE_DIR / '.env')

# engine = create_async_engine(
#     URL.create(
#         drivername=settings.DRIVER,
#         host=settings.HOST,
#         database=settings.POSTGRES_DB,
#         username=settings.POSTGRES_USER,
#         password=settings.POSTGRES_PASSWORD,
#         port=settings.PORT
#     )
#
if settings.MODE == 'TEST':
    DATABASE_URL = settings.test_database_url
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.database_url
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# class Base(DeclarativeBase):
#     pass

class Base(DeclarativeBase):
    pass
