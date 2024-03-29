from typing import Annotated
import uuid
import aiofiles
from click import File

from fastapi import APIRouter, Depends, Form, Path, Request, Response, UploadFile
from pydantic import BaseModel, HttpUrl, EmailStr

from app.companies.dao import CityDAO, CompanyDAO
from app.companies.models import Company
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.schemas import ProfileUser
from app.vacancies.models import City
from app.users.models import Resume, User


router = APIRouter(prefix="/company", tags=["Компании"])


class CompanyModel(BaseModel):
    name: Annotated[str, Form()]
    url: Annotated[HttpUrl, Form()]
    city_id: Annotated[int, Form()]
    phone: Annotated[int, Form()]
    email: Annotated[EmailStr, Form()]
    about_company: Annotated[str, Form()]


@router.post("/create", status_code=201)
async def create_company(
    logo: Annotated[UploadFile | None, File()],
    name: Annotated[str, Form()],
    url: Annotated[HttpUrl, Form()],
    city_id: Annotated[int, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    user: Annotated[ProfileUser, Depends(get_current_user)],
    about_company: Annotated[str | None, Form()] = None
):
    ext: str = logo.filename.rsplit(".")[-1]
    logo_path = f"images/company_logo/{str(uuid.uuid4())}.{ext}"

    async with aiofiles.open(logo_path, "wb") as f:
        await f.write(logo.file.read())
    new_company_data = {
        "logo": logo_path,
        "name": name,
        "url": str(url),
        "city_id": city_id,
        "phone": phone,
        "email": email,
        "about_company": about_company,
        "user_id": user.id,
    }
    new_company_id = await CompanyDAO.create(Company, **new_company_data)
    return {'id': new_company_id}


@router.get("/cities", status_code=200)
async def get_cities():
    result = await CityDAO.get_list(City)
    return result


@router.get('/{company_id}', status_code=200)
async def get_company(
    company_id: Annotated[int, Path()], 
    request: Request
):
    token = request.headers.get('Authorization')
    user = await get_current_user(token=token) if token else None
    result = await CompanyDAO.get_company_with_all_data(company_id)
    return {
        'company': result,
        'is_owner': result.owner.username == user.username if user else False
    }
    

@router.get('/check_owner_company/{company_id}', status_code=200)
async def check_owner_company(
    company_id: int,
    user: Annotated[ProfileUser, Depends(get_current_user)]
) -> dict[str, bool]:
    user: User = await UserDAO.get_user(user.username)
    return {
        'is_owner': company_id in [c.id for c in user.companies]
    }