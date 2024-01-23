from fastapi import APIRouter
from sqlalchemy import select

from fastapi_learning.app.rooms.models import Rooms
from fastapi_learning.app.database import async_session_maker

router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)


@router.get('')
async def get_users():
    async with async_session_maker() as session:
        query = select(Rooms)

        result = await session.execute(query)
        result = result.mappings().all()
        return result