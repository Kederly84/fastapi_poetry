from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict

from fastapi_learning.app.bookings.schemas import SBooking


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    email: EmailStr
    hashed_password: str
    bookings: Optional[List[SBooking]] = None
