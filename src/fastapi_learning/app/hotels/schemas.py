from typing import List

from pydantic import BaseModel, ConfigDict


class SHotels(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int


class SHotelsByLocation(SHotels):
    rooms_left: int
