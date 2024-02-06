import shutil
from pathlib import Path

from fastapi import UploadFile, APIRouter

from fastapi_learning.app.tasks.tasks import img_resize

router = APIRouter(
    prefix="/images",
    tags=["images upload"]
)

BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "static/images"


@router.post("/hotels")
async def add_hotels_image(name: int, file: UploadFile):
    img_path = f'{path}/{name}.webp'
    with open(img_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    img_resize.delay(img_path)
