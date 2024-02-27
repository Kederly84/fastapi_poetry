from dataclasses import dataclass
from datetime import date

from sqlalchemy import ForeignKey, Date, Computed, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_learning.app.database import Base


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

@dataclass
class BookingData:
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed('(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Computed('(date_to - date_from)'))
    user: Mapped["Users"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship(back_populates="bookings")

    def convert_to_data(self):
        return BookingData(
            id=self.id,
            room_id=self.room_id,
            user_id=self.user_id,
            date_from=self.date_from,
            date_to=self.date_to,
            price=self.price,
            total_cost=self.total_cost,
            total_days=self.total_days
        )

    def __str__(self):
        return f"BookingData: {self.id}, {self.date_from}, {self.date_to}"
