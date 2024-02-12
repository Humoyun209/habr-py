from pprint import pprint
from fastapi import APIRouter
from app.companies.models import Company
from app.vacancies.dao import VacancyDAO
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
async def create_vacancy(vm: VacancyModel):
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
