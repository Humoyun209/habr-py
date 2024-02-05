from typing import Annotated
import uuid
import aiofiles
from click import File

from fastapi import APIRouter, Depends, Form, UploadFile
from pydantic import BaseModel, HttpUrl, EmailStr

from app.companies.dao import CityDAO, CompanyDAO
from app.companies.models import Company
from app.users.dependencies import get_current_user
from app.users.schemas import ProfileUser
from app.vacancies.models import City


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
    logo: Annotated[UploadFile, File()],
    name: Annotated[str, Form()],
    url: Annotated[HttpUrl, Form()],
    city_id: Annotated[int, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    about_company: Annotated[str, Form()],
    user: Annotated[ProfileUser, Depends(get_current_user)],
):
    ext: str = logo.filename.rsplit(".")[-1]
    logo_path = f"images/company_logo/{str(uuid.uuid4())}.{ext}"

    async with aiofiles.open(logo_path, "wb") as f:
        await f.write(logo.file.read())
    new_company_data = {
        "photo": logo_path,
        "name": name,
        "url": str(url),
        "city_id": city_id,
        "phone": phone,
        "email": email,
        "about_company": about_company,
        "user_id": user.id,
    }
    new_company = await CompanyDAO.create(Company, **new_company_data)
    return new_company


@router.get("/cities", status_code=200)
async def get_cities():
    return await CityDAO.get_list(City)


@router.get('/company/{company_id}')
async def get_logo_company(company_id):
    return 
