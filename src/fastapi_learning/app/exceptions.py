from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User Already Exists'


class UnauthorizedException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Unauthorized'


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'


class WrongTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Wrong token'


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Room cannot be booked'


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"


class CannotDeleteBookingException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Booking does not exist"
