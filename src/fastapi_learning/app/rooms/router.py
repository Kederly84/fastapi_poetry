from datetime import date
from typing import List

from fastapi import APIRouter

from fastapi_learning.app.rooms.dao import RoomsDAO
from fastapi_learning.app.rooms.schemas import SRoomInfo, SRoom

router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)


@router.get('')
async def get_rooms() -> List[SRoom]:
    rooms = await RoomsDAO.find_all()
    return rooms


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_hotel_id(hotel_id: int, date_from: date, date_to: date) -> List[SRoomInfo]:
    rooms = await RoomsDAO.find_by_hotel(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return rooms
