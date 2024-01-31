from sqladmin import ModelView
from app.companies.models import Company

from app.users.models import Resume, User
from app.vacancies.models import City, Vacancy


class UserAdmin(ModelView, model=User):
    column_exclude_list = [User.password]
    icon = "fa-solid fa-user"
    

class CompanyAdmin(ModelView, model=Company):
    column_exclude_list = [User.password]
    icon = "fa-solid fa-school"
    name_plural = "Companies"


class VacancyAdmin(ModelView, model=Vacancy):
    column_exclude_list = [User.password]
    icon = "fa-solid fa-tasks"
    name_plural = 'Vacancies'

class ResumeAdmin(ModelView, model=Resume):
    column_exclude_list = [User.password]
    icon = "fa-regular fa-file"


class CityAdmin(ModelView, model=City):
    column_exclude_list = [User.password]
    icon = "fa-solid fa-city"
    name_plural = 'Cities'