from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from fastapi_learning.app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    booking = relationship('Bookings', back_populates='user')
