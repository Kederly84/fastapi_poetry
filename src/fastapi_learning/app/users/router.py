from typing import List, Optional, Union

from fastapi import APIRouter, HTTPException, status, Response

from fastapi_learning.app.users.auth import get_password_hash, authenticate_user, create_access_token
from fastapi_learning.app.users.dao import UsersDAO
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
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    result = await UsersDAO.create(email=user_data.email, hashed_password=hashed_password)
    return result.id


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect")
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    user = await UsersDAO.find_one_or_none()
