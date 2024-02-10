from decimal import Decimal
from fastapi import HTTPException
from pydantic import BaseModel, model_validator, ValidationError

from app.users.enums import Level, WorkLoad


class VacancyModel(BaseModel):
    title: str
    min_salary: Decimal
    max_salary: Decimal
    expectation: str
    conditions: str
    bonuses: str | None
    workload: WorkLoad
    level: Level
    is_remote: bool
    company_id: int
    city_id: int
    company_id: int
    tags: list[str]
    
    @model_validator
    def check_fields(cls, nv: "VacancyModel"):
        if nv.min_salary or nv.max_salary:
            raise HTTPException(401, "Должна быть заполнено поля заработной платы")
        if len(nv.tags) < 4:
            raise HTTPException(401, "Укажите хотя бы одного навыка")
        return nv
        
    
    