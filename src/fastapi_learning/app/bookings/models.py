from sqlalchemy import Column, Integer, ForeignKey, Date, Computed, BigInteger
from sqlalchemy.orm import relationship

from fastapi_learning.app.database import Base


class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(BigInteger, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
    total_days = Column(Integer, Computed('(date_to - date_from)'))
    rooms = relationship('Rooms', back_populates='booking')
    user = relationship('Users', back_populates='booking')
