from fastapi import APIRouter

from app.vacancies.schemas import VacancyModel


router = APIRouter(prefix="/vacancy", tags=["Вакансии"], )


@router.get("/create", status_code=201)
async def create_vacancy(vm: VacancyModel):
    pass