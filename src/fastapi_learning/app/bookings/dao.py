from datetime import date

from sqlalchemy import select, and_, or_, func, insert

from fastapi_learning.app.bookings.models import Bookings
from fastapi_learning.app.dao.base import BaseDAO
from fastapi_learning.app.database import async_session_maker, engine
from fastapi_learning.app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, room_id: int, user_id: int, date_from: date, date_to: date):
        """
        In code release this example SQL expressions
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
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
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(
                Rooms.id == room_id
            ).group_by(
                Rooms.quantity,
                booked_rooms.c.room_id
            )
            # This code just print SQL expression from SQLAlchemy
            print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            print(rooms_left)
            print(type(rooms_left))
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_bookind = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings.__table__.columns)
                new_booking = await session.execute(add_bookind)

                await session.commit()
                return new_booking.mappings().one()
            else:
                return None

    @classmethod
    async def find_bookings(cls, user_id: int):
        async with async_session_maker() as session:
            stmt = (
                select(
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                ).join(
                    Rooms,
                    Rooms.id == Bookings.room_id,
                    isouter=True
                ).where(
                    Bookings.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            result = result.mappings().all()
            return result
