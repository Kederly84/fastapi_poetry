from fastapi_learning.app.dao.base import BaseDAO
from fastapi_learning.app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
