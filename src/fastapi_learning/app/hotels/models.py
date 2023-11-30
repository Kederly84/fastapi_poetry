from sqlalchemy import Column, Integer, String, JSON, BigInteger
from sqlalchemy.orm import relationship

from fastapi_learning.app.database import Base


class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
    rooms = relationship('Rooms', back_populates='hotel')
