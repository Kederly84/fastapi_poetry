from datetime import date
from typing import List, Union

from fastapi import APIRouter, Depends

from fastapi_learning.app.bookings.dao import BookingDAO
from fastapi_learning.app.bookings.schemas import SBooking, SBookingInfo, SNewBooking
from fastapi_learning.app.exceptions import RoomCannotBeBooked, WrongTokenException, CannotDeleteBookingException
from fastapi_learning.app.users.dependencies import get_current_user
from fastapi_learning.app.users.models import Users

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
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookingInfo]:
    bookings = await BookingDAO.find_bookings(user_id=user.id)
    return bookings


@router.get('/{booking_id}')
async def get_bookings(booking_id: int) -> SBooking:
    booking = await BookingDAO.find_one_or_none(id=booking_id)
    return booking


@router.post('/add_booking')
async def add_booking(room_id: int,
                      date_from: date,
                      date_to: date,
                      user: Users = Depends(get_current_user)
                      ) -> Union[SNewBooking, str]:
    try:
        user_id = int(user.id)
    except AttributeError:
        return f'{WrongTokenException.detail}'

    booking = await BookingDAO.add(
        room_id=room_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to
    )
    if booking:
        print(booking)
        return booking
    else:
        raise RoomCannotBeBooked


@router.delete('/{booking_id}/delete_booking')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    try:
        user_id = int(user.id)
    except AttributeError:
        return f'{WrongTokenException.detail}'
    booking = await BookingDAO.delete(id=booking_id, user_id=user_id)
    if booking:
        return booking
    else:
        raise CannotDeleteBookingException
