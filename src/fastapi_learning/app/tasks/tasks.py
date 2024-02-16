import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from fastapi_learning.app.config import settings
from fastapi_learning.app.tasks.celery_app import celery_app
from fastapi_learning.app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def img_resize(img_path: str):
    img_path = Path(img_path)
    im = Image.open(img_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f'{img_path.parent}/resized_1000_500_{img_path.name}')
    im_resized_200_100.save(f'{img_path.parent}/resized_200_100_{img_path.name}')


@celery_app.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
