from sqladmin import ModelView

from fastapi_learning.app.bookings.models import Bookings
from fastapi_learning.app.hotels.models import Hotels
from fastapi_learning.app.rooms.models import Rooms
from fastapi_learning.app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class BookingsAdmin(ModelView, model=Bookings):
    # column_list = [columns.name for columns in Bookings.__table__.columns]
    # column_list = '__all__'
    column_exclude_list = [Bookings.id, Bookings.user_id, Bookings.room_id]
    can_delete = False
    name = 'Бронирование'
    name_plural = 'Бронирования'
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"
