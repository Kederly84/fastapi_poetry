from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from fastapi_learning.app.hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Фронт"]
)

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get('/hotels')
async def get_hotels_page(
        request: Request,
        hotels: Depends = Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={
            "request": request,
            "hotels": hotels
        })
