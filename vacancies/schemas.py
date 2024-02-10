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
    company_id: int
    tags: list[int]
    
    @model_validator(mode='after')
    def check_fields(cls, nv: "VacancyModel"):
        if len(nv.tags) < 4:
            raise HTTPException(401, "Укажите хотя бы одного навыка")
        return nv
        
    
    