from fastapi import APIRouter
from sqlalchemy import select

from fastapi_learning.app.hotels.models import Hotels
from fastapi_learning.app.database import async_session_maker

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('')
async def get_hotels():
    async with async_session_maker() as session:
        query = select(Hotels)

        result = await session.execute(query)
        result = result.mappings().all()
        return result
