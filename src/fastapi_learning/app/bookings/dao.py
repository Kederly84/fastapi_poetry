from fastapi_learning.app.database import async_session_maker
from sqlalchemy import select
from fastapi_learning.app.bookings.models import Bookings
from fastapi_learning.app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
    # @classmethod
    # async def find_all(cls):
    #     async with async_session_maker() as session:
    #         stmt = select(Bookings.__table__.columns)
    #         bookings = await session.execute(stmt)
    #         result = bookings.mappings().all()
    #         return result
