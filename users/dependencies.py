from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from app.companies.dao import CompanyDAO
from app.users.dao import UserDAO

from app.config import get_secret
from app.users.models import User
from app.users.schemas import ProfileUser


async def check_owner_company(user_id, company_id):
    company_ids = await CompanyDAO.company_ids(user_id)
    return company_id in company_ids


def get_token(request: Request):
    token = request.headers.get('Authorization')
    try:
        key, access_token = token.split()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if key == 'Bearer' and access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return access_token


async def get_current_user(token: Annotated[str, Depends(get_token)]) -> ProfileUser:
    try:
        payload = jwt.decode(
            token=token,
            key=get_secret().PUBLIC_KEY,
            algorithms=get_secret().ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Токен не действителен')
    exp = payload.get('exp')
    username = payload.get('sub')
    if not exp or not username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Нужные аттрибуты не найдены в токене')
    if int(exp) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Срок токена истек')
    data: User = await UserDAO.get_user(username)
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return ProfileUser(
        id=data.id,
        username=data.username,
        email=data.email
    )
