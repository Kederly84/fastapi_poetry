from datetime import datetime

from fastapi import Request, Depends
from jose import JWTError, jwt

from fastapi_learning.app.config import settings
from fastapi_learning.app.exceptions import WrongTokenException, \
    TokenExpiredException, UnauthorizedException
from fastapi_learning.app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise UnauthorizedException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
    except JWTError:
        return WrongTokenException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UnauthorizedException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UnauthorizedException
    return user
