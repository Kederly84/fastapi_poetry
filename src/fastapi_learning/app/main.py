from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from uvicorn import run

from fastapi_learning.app.bookings.router import router as router_bookings
from fastapi_learning.app.hotels.router import router as router_hotels
from fastapi_learning.app.images.router import router as router_images
from fastapi_learning.app.pages.router import router as router_pages
from fastapi_learning.app.rooms.router import router as router_rooms
from fastapi_learning.app.users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)


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


# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Authorization",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origins"]
)


def main():
    run(
        'src.fastapi_learning.app.main:app',
        port=8000,
        host='127.0.0.1',
        reload=True
    )


if __name__ == '__main__':
    main()
