from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.companies.dao import CompanyDAO

from app.users.dao import UserDAO
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.schemas import UserLogin, UserScheme, ProfileUser
from passlib.hash import pbkdf2_sha256

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/list', status_code=200)
async def get_list_users():
    users = [
        ProfileUser(id=user[0], username=user[1], email=user[2])
        for user in await UserDAO.get_users()
    ]
    return users


@router.post('/register')
async def create_user(user: UserScheme):
    if user is None:
        raise HTTPException(status_code=400, detail='Пароли не совпадают')
    result = await UserDAO.create_user(
        username=user.username,
        email=user.email,
        password=pbkdf2_sha256.hash(user.password)
    )
    if result:
        access_token = create_access_token({'sub': user.username})
        return {'access_token': access_token}
    else:
        raise HTTPException(status_code=400, detail='Пользователь с таким эмейлом существует')
    

@router.post('/login')
async def login_user(user: UserLogin):
    user = await authenticate_user(user.username, user.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({'sub': user.username})
    return {'access_token': access_token}


@router.get('/profile')
async def get_profile(
    user: Annotated[ProfileUser, Depends(get_current_user)]
):
    return user