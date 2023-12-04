import typing
from datetime import date

from sqlalchemy import ForeignKey, Date, Computed, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column

from fastapi_learning.app.database import Base

if typing.TYPE_CHECKING:
    from fastapi_learning.app.rooms.models import Rooms
    from fastapi_learning.app.users.models import Users


# class Bookings(Base):
#     __tablename__ = 'bookings'
#
#     id = Column(BigInteger, primary_key=True)
#     room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     date_from = Column(Date, nullable=False)
#     date_to = Column(Date, nullable=False)
#     price = Column(Integer, nullable=False)
#     total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
#     total_days = Column(Integer, Computed('(date_to - date_from)'))
#     rooms = relationship('Rooms', back_populates='booking')
#     user = relationship('Users', back_populates='booking')


class Bookings(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    date_from: Mapped[date] = mapped_column(nullable=False)
    date_to: Mapped[date] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed('(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Computed('(date_to - date_from)'))
    rooms: Mapped['Rooms'] = relationship(back_populates='booking')
    user: Mapped['Users'] = relationship(back_populates='booking')
