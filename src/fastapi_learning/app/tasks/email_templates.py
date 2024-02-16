from email.message import EmailMessage
from fastapi_learning.app.config import settings
from pydantic import EmailStr


def create_booking_confirmation_template(
        booking: dict,
        email: EmailStr
) -> EmailMessage:
    email_message = EmailMessage()
    email_message['Subject'] = 'Booking confirmation'
    email_message['From'] = settings.SMTP_USER
    email_message['To'] = email
    email_message.set_content(
        f'''
        <h1>Booking confirmation</h1>
        Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        ''',
        subtype='html'
    )
    return email_message
