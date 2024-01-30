from typing import List

from fastapi import APIRouter, Response, Depends
from sqlalchemy.testing.pickleable import User

from fastapi_learning.app.exceptions import UserAlreadyExistsException, \
    UnauthorizedException
from fastapi_learning.app.users.auth import get_password_hash, authenticate_user, create_access_token
from fastapi_learning.app.users.dao import UsersDAO
from fastapi_learning.app.users.dependencies import get_current_user
from fastapi_learning.app.users.schemas import SUserAuth, SUser

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.get('')
async def get_users() -> List[SUser]:
    result = await UsersDAO.find_all()
    return result


@router.post('/register')
async def register_user(user_data: SUserAuth) -> int:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    result = await UsersDAO.create(email=user_data.email, hashed_password=hashed_password)
    return result.id


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise UnauthorizedException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/current_user')
async def current_user(user: User = Depends(get_current_user)):
    if user:
        return user
