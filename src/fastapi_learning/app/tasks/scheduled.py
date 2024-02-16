import smtplib
from datetime import datetime, timedelta

from sqlalchemy import select

from fastapi_learning.app.bookings.models import Bookings
from fastapi_learning.app.config import settings
from fastapi_learning.app.tasks.celery_app import celery_app, sync_session
from fastapi_learning.app.tasks.email_templates import create_booking_confirmation_template
from fastapi_learning.app.users.models import Users
from fastapi_learning.app.rooms.models import Rooms
from fastapi_learning.app.hotels.models import Hotels


@celery_app.task(name="scheduled_task")
def scheduled_task():
    print('12345')


@celery_app.task(name="send_booking_tomorrow_alert_email")
def send_booking_tomorrow_alert_email(days: int = 3):
    with sync_session() as session:
        tomorrow = datetime.now().date() + timedelta(days=days)
        print(tomorrow)
        stmt = select(
            Bookings.__table__.columns, Users.email
        ).join(
            Users,
            Bookings.user_id == Users.id,
            isouter=True
        ).where(Bookings.date_from == tomorrow)
        bookings = session.execute(stmt)
        bookings = bookings.mappings().all()
    bookings = list(map(lambda x: dict(x), bookings))
    print(bookings)
    if bookings:
        for booking in bookings:
            msg_content = create_booking_confirmation_template(booking=booking, email=booking['email'])
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg_content)
    else:
        print("No booking")

