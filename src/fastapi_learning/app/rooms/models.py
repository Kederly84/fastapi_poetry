from sqlalchemy import (
    ForeignKey,
    JSON,
    BigInteger)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from fastapi_learning.app.database import Base

import typing

if typing.TYPE_CHECKING:
    from fastapi_learning.app.hotels.models import Hotels


# class Rooms(Base):
#     __tablename__ = 'rooms'
#
#     id = Column(BigInteger, primary_key=True)
#     hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=True)
#     price = Column(Integer, nullable=False)
#     services = Column(JSON)
#     quantity = Column(Integer, nullable=False)
#     image_id = Column(BigInteger, nullable=True)
#     hotel = relationship(
#         'Hotels',
#         back_populates='room',
#         cascade='all, delete'
#     )
#     booking = relationship('Bookings', back_populates='room')


class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f'{self.name} - {self.description}'
