from pprint import pprint
from typing import Annotated
from fastapi import APIRouter, Depends, Path
from app.companies.models import Company
from app.users.dependencies import get_current_user
from app.users.schemas import ProfileUser
from app.vacancies.dao import ResponseDAO, VacancyDAO
from app.vacancies.models import Tag, Vacancy

from app.vacancies.schemas import VacancyModel


router = APIRouter(
    prefix="/vacancy",
    tags=["Вакансии"],
)


@router.get("/list", status_code=200)
async def get_vacancies():
    vacancies = await VacancyDAO.get_vacancies()
    return vacancies


@router.post("/create", status_code=201)
async def create_vacancy(
    vm: VacancyModel, user: Annotated[ProfileUser, Depends(get_current_user)]
):
    company = await VacancyDAO.get(Company, vm.company_id)
    new_vacancy = vm.model_dump() | {"city_id": company.city_id}
    tags = await VacancyDAO.get_tags_by_ids(vm.tags)
    del new_vacancy["tags"]

    vacancy_id = await VacancyDAO.create_vacancy(new_vacancy)
    await VacancyDAO.add_tags(tags, vacancy_id)
    return vacancy_id


@router.get("/tags", status_code=200)
async def get_tags():
    tags = await VacancyDAO.get_list(Tag)
    return tags


@router.get("/{vacancy_id}", status_code=200)
async def get_vacancy(vacancy_id: int):
    data = await VacancyDAO.get_vacancy(vacancy_id)
    return data


@router.post("/{vacancy_id}/respond")
async def respond_to_vacancy(
    vacancy_id: Annotated[int, Path(gt=0)],
    user: Annotated[ProfileUser, Depends(get_current_user)],
    cover_letter: str | None = None,
):
    response = await ResponseDAO.create_response(
        user_id=user.id, vacancy_id=vacancy_id, cover_letter=cover_letter
    )
    return response
