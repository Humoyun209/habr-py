from datetime import datetime
from decimal import Decimal
from pydantic import (
    BaseModel,
    EmailStr,
    model_validator,
    ValidationError,
    field_validator,
)


class UserScheme(BaseModel):
    username: str
    email: EmailStr
    password: str
    password2: str

    @model_validator(mode="after")
    def root_validate(cls, user: "UserScheme"):
        if user.password != user.password2:
            return None
        return user


class UserLogin(BaseModel):
    username: str
    password: str


class ProfileUser(BaseModel):
    id: int
    username: str
    email: EmailStr


class BaseResume(BaseModel):
    first_name: str
    last_name: str
    phone: str
    about: str
    experience: str | None
    birthday: datetime
    sex: int
    salary: Decimal | None

    @field_validator("birthday", mode="before")
    def validate_birthday(cls, value: str):
        try:
            birthday = datetime.strptime(value, "%Y-%m-%d")
        except Exception as e:
            raise ValidationError("Данные рождения не правильно отправляется")
        return birthday

    @model_validator(mode="after")
    def validate(cls, resume: "BaseResume"):
        if resume.sex not in [0, 1]:
            raise ValidationError("Sex should be 0 and 1")
        return resume
    

class ResumeSchema(BaseModel):
    
