from datetime import date

from sqlalchemy import select, and_, or_, func

from fastapi_learning.app.bookings.models import Bookings
from fastapi_learning.app.dao.base import BaseDAO
from fastapi_learning.app.database import async_session_maker, engine
from fastapi_learning.app.hotels.models import Hotels
from fastapi_learning.app.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_by_location(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            hotels_avail = select(
                Hotels.__table__.columns
            ).filter(
                Hotels.location.like(f"%{location}%")
            ).cte('hotels_avail')
            hotel_rooms = select(
                Rooms.__table__.columns
            ).where(
                Rooms.hotel_id == hotels_avail.c.id
            ).cte('hotel_rooms')
            booked_rooms = select(Bookings.__table__.columns).where(
                and_(
                    Bookings.room_id == hotel_rooms.c.id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')
            get_rooms_left = select(
                hotel_rooms.c.hotel_id,
                (hotel_rooms.c.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(hotel_rooms).join(
                booked_rooms,
                booked_rooms.c.room_id == hotel_rooms.c.id,
                isouter=True
            ).group_by(
                hotel_rooms.c.quantity,
                booked_rooms.c.room_id,
                hotel_rooms.c.hotel_id
            ).cte('get_rooms_left')
            rooms_left = select(
                get_rooms_left.c.hotel_id,
                func.sum(get_rooms_left.c.rooms_left).label('rooms_left')
            ).group_by(
                get_rooms_left.c.hotel_id
            ).cte('rooms_left')
            hotels = select(
                Hotels.__table__.columns,
                rooms_left.c.rooms_left
            ).join(
                rooms_left,
                rooms_left.c.hotel_id == Hotels.id,
                isouter=True
            ).where(
                rooms_left.c.rooms_left > 0
            )
            print(hotels.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels = await session.execute(hotels)
            hotels = hotels.mappings().all()
            # print(hotels)
            return hotels

    @classmethod
    async def find_all_by_location(cls, location: str, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            GROUP BY hotel_id
        )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%';
        """
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        booked_hotels = (
            select(Rooms.hotel_id, func.sum(
                Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%"),
                )
            )
        )
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
