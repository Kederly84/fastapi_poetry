from typing import List, Optional

from fastapi import APIRouter, Depends

from fastapi_learning.app.bookings.dao import BookingDAO
from fastapi_learning.app.bookings.schemas import SBooking
from fastapi_learning.app.users.dependencies import get_current_user
from fastapi_learning.app.users.models import Users
from fastapi_learning.app.users.schemas import SUser

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


# @router.get('')
# async def get_bookings():
#     async with async_session_maker() as session:
        # query = select(Bookings).options(selectinload(Bookings.user).options(load_only(Users.id, Users.email)),
        #                                  defer(Bookings.user_id),
        #                                  selectinload(Bookings.room).options(selectinload(Rooms.hotel),
        #                                                                      defer(Rooms.hotel_id)),
        #                                  defer(Bookings.room_id))
        # user = aliased(Users, name='user')
        # query = select(Bookings.__table__.columns, user).join(user).options(load_only(user.id, user.email))
        # query = select(Bookings).join(Users)
        # query = select(Bookings, Users).join(Bookings.user, full=True)
        # query = select(Bookings)
        # print(query)
        # res = await session.execute(query)
        # print(res)
        # result = res.scalars().all()
        # print(result)
        # print(isinstance(result[0][0], Bookings))
        # print(isinstance(result[0][1], Users))
        # return result

# asyncio.run(get_bookings())

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBooking]:
    bookings = await BookingDAO.find_all(user_id=int(user.id))
    return bookings



@router.get('/{booking_id}')
async def get_bookings(booking_id: int) -> SBooking:
    ask = {'id': booking_id}
    booking = await BookingDAO.find_one_or_none(**ask)
    return booking
