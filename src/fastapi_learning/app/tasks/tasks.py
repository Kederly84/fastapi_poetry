from pathlib import Path

from fastapi_learning.app.tasks.celery_app import celery_app
from PIL import Image


@celery_app.task
def img_resize(img_path: str):
    img_path = Path(img_path)
    im = Image.open(img_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f'{img_path.parent}/resized_1000_500_{img_path.name}')
    im_resized_200_100.save(f'{img_path.parent}/resized_200_100_{img_path.name}')
