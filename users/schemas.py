from datetime import datetime
from decimal import Decimal
from pydantic import (
    BaseModel,
    EmailStr,
    model_validator,
    ValidationError,
    field_validator,
)

from app.users.enums import ConnectType, Level, WorkLoad


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


class TokenModel(BaseModel):
    access_token: str
    token_type: str


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


class ResumeSchema(BaseResume):
    tags: list[int]
    connect_type: ConnectType | None
    connect_link: str | None
    workload: WorkLoad
    level: Level
    is_remote: bool
    cities: list[int]

    @field_validator("tags", mode="before")
    def validate_birthday(cls, value: list[int]):
        if len(value) < 4:
            raise ValidationError("Укажите минимум 4 навыка")
        return value

    @model_validator(mode="after")
    def validate(cls, resume: "ResumeSchema"):
        if all([resume.connect_type, resume.connect_link]) or all(
            [not resume.connect_type, not resume.connect_link]
        ):
            return resume
        return resume
