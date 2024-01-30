from sqlalchemy import JSON, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column

from fastapi_learning.app.database import Base


# class Hotels(Base):
#     __tablename__ = 'hotels'
#
#     id = Column(BigInteger, primary_key=True)
#     name = Column(String, nullable=False)
#     location = Column(String, nullable=False)
#     services = Column(JSON)
#     rooms_quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)
#     rooms = relationship('Rooms', back_populates='hotel')


class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]
    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")
