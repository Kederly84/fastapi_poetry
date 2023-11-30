from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Text,
    Integer,
    JSON,
    BigInteger)
from sqlalchemy.orm import relationship

from fastapi_learning.app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(BigInteger, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(BigInteger, nullable=True)
    hotel = relationship(
        'Hotels',
        back_populates='room',
        cascade='all, delete'
    )
    booking = relationship('Bookings', back_populates='room')
