from datetime import date
from typing import Annotated, Optional

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from uvicorn import run

from fastapi_learning.app.bookings.router import router as router_bookings
from fastapi_learning.app.users.router import router as router_users
from fastapi_learning.app.hotels.router import router as router_hotels
from fastapi_learning.app.rooms.router import router as router_rooms

app = FastAPI()
app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)


# print(Base.metadata.tables)
# class Hotel(BaseModel):
#     hotel: str
#     location: str
#     date_from: date
#     date_to: date
#     has_spa: Optional[bool] = False
#     stars: Optional[int] = None
#
#
# class HotelSearchArgs:
#     def __init__(self,
#                  location: str,
#                  date_from: date,
#                  date_to: date,
#                  has_spa: bool = False,
#                  stars: int = Query(None, ge=1, le=5)
#                  ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars
#
#
# @app.get('/hotels')
# def get_hotels(
#         req_params: Annotated[HotelSearchArgs, Depends(HotelSearchArgs)]
# ) -> Hotel:
#     res = {
#         'hotel': 'Some hotel',
#         'location': str(req_params.location),
#         'date_from': req_params.date_from,
#         'date_to': req_params.date_to,
#         'has_spa': req_params.has_spa,
#         'stars': req_params.stars
#     }
#     hotel = Hotel(**res)
#     return hotel


def main():
    run(
        'src.fastapi_learning.app.main:app',
        port=8000,
        host='127.0.0.1',
        reload=True
    )


if __name__ == '__main__':
    main()
