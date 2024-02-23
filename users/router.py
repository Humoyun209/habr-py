import json
import secrets
from typing import Annotated, Any
import uuid
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Form,
    HTTPException,
    Header,
    Path,
    Request,
    Response,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.companies.dao import CompanyDAO

from app.users.dao import ResumeDAO, UserDAO
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Resume
from app.users.schemas import BaseResume, UserLogin, UserScheme, ProfileUser
from passlib.hash import pbkdf2_sha256

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/list", status_code=200)
async def get_list_users():
    users = [
        ProfileUser(id=user[0], username=user[1], email=user[2])
        for user in await UserDAO.get_users()
    ]
    return users


@router.post("/register")
async def create_user(user: UserScheme):
    if user is None:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    result = await UserDAO.create_user(
        username=user.username,
        email=user.email,
        password=pbkdf2_sha256.hash(user.password),
    )
    if result:
        access_token = create_access_token({"sub": user.username})
        return {"access_token": access_token}
    else:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким эмейлом существует"
        )


@router.post("/login")
async def login_user(user: UserLogin):
    user = await authenticate_user(user.username, user.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token}


@router.get("/profile")
async def get_profile(user: Annotated[ProfileUser, Depends(get_current_user)]):
    full_user = await UserDAO.get_full_data_user(user.id)
    return full_user


@router.post("/resume/create")
async def create_resume(
    user: Annotated[ProfileUser, Depends(get_current_user)], base_resume: BaseResume
):
    data = base_resume.model_dump() | {"user_id": user.id}
    resume = await ResumeDAO.create_resume(**data)
    return resume


@router.get("/resume/{resume_id}", status_code=200)
async def get_resume(
    user: Annotated[ProfileUser, Depends(get_current_user)],
    resume_id: Annotated[int, Path()],
):
    resume = await ResumeDAO.get(Resume, resume_id)
    return resume


@router.patch("/resume/edit", status_code=204)
async def resume_edit(
    resume_data: ResumeSchema,
    Annotated
)