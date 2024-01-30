from datetime import date
from typing import List

from fastapi import APIRouter

from fastapi_learning.app.hotels.dao import HotelDAO
from fastapi_learning.app.hotels.schemas import SHotelsByLocation, SHotels
from fastapi_learning.app.rooms.dao import RoomsDAO
from fastapi_learning.app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('')
async def get_hotels() -> List[SHotels]:
    hotels = await HotelDAO.find_all()
    return hotels


@router.get('/{location}')
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date,
        date_to: date) -> List[SHotelsByLocation]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get('/id/{hotel_id}/')
async def get_rooms_by_hotel(hotel_id: int) -> SHotels:
    rooms = await HotelDAO.find_one_or_none(id=hotel_id)
    return rooms
