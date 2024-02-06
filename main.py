from typing import Annotated
from fastapi import Cookie, Depends, FastAPI, HTTPException, Header, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from app.admin.admin import CityAdmin, CompanyAdmin, ResumeAdmin, UserAdmin, VacancyAdmin
from app.users.router import router as user_router
from app.companies.router import router as company_router
from app.database import engine
from app.admin.auth import authentication_backend

app = FastAPI()
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(CompanyAdmin)
admin.add_view(VacancyAdmin)
admin.add_view(CityAdmin)
admin.add_view(ResumeAdmin)

app.include_router(user_router)
app.include_router(company_router)
app.mount('/images', StaticFiles(directory='./images'), 'static')

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_home(name: Annotated[str | None, Query()]):
    return {'Message': f'Welcome to Full Stack - {name}'}
