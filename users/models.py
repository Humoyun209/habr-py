from decimal import Decimal
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base
from app.users.enums import Level, WorkLoad


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    favorited_vacancies: Mapped[list['Vacancy']] = relationship(
        back_populates='favorited_workers',
        secondary='workers_favorited_vacancies'
    )
    companies: Mapped[list["Company"]] = relationship(
        back_populates="owner"
    )
    followed_companies: Mapped[list["Company"]] = relationship(
        back_populates="followers",
        secondary="companies_followers"
    )
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user")
    

    def __repr__(self) -> str:
        return f"User - {self.username}"


class Resume(Base):
    __tablename__ = 'resume'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    photo: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    about: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    salary: Mapped[Decimal | None]
    workload: Mapped[WorkLoad]
    level: Mapped[Level]
    cities: Mapped[list['City']] = relationship(back_populates="resumes", secondary="cities_resumes")
    user: Mapped["User"] = relationship(back_populates="resumes")
    tags: Mapped[list["Tag"]] = relationship(back_populates="resumes", secondary="tags_resumes")
    vacancies: Mapped[list["Vacancy"]] = relationship(
        back_populates="resumes",
        secondary="responses"
    )
    
    def __repr__(self) -> str:
        return f'Resume by {self.first_name} {self.last_name}'


class TagsResumes(Base):
    __tablename__ = "tags_resumes"
    
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tag.id', ondelete='CASCADE'),
        primary_key=True
    )
    resume_id: Mapped[int] = mapped_column(
        ForeignKey('resume.id', ondelete='CASCADE'),
        primary_key=True
    )


class WorkersFavoritedVacancies(Base):
    __tablename__ = 'workers_favorited_vacancies'
    
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey('vacancy.id', ondelete='CASCADE'), 
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )


