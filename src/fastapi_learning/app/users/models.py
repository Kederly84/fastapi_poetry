from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, mapped_column, Mapped
import typing

from fastapi_learning.app.database import Base

if typing.TYPE_CHECKING:
    from fastapi_learning.app.bookings.models import Bookings


# class Users(Base):
#     __tablename__ = 'users'
#
#     id = Column(BigInteger, primary_key=True)
#     email = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     booking = relationship('Bookings', back_populates='user')


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f'{self.email}'
