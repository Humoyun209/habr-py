from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, ForeignKey, text
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    resumes: Mapped[list['Resume']] = relationship(back_populates='cities', secondary='cities_resumes')

    def __repr__(self) -> str:
        return self.name


class Tag(Base):
    __tablename__ = 'tag'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    resumes: Mapped[list["Resume"]] = relationship(back_populates="tags", secondary="tags_resumes")
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="tags", secondary="tags_vacancies")
    
    def __repr__(self) -> str:
        return f'Tag #{self.name}'


class Vacancy(Base):
    __tablename__ = 'vacancy'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    min_salary: Mapped[Decimal]
    max_salary: Mapped[Decimal | None]
    about_company: Mapped[str | None]
    candidate_expectation: Mapped[str | None]
    working_conditions: Mapped[str | None]
    bonuses: Mapped[str | None]
    created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"))
    city_id: Mapped[int | None] = mapped_column(ForeignKey("city.id", ondelete="SET NULL"))
    company: Mapped["Company"] = relationship(back_populates="vacancies")
    workloads: Mapped[list["WorkLoad"]] = relationship(
        back_populates="vacancies",
        secondary="workloads_vacancies"
    )
    favorited_workers: Mapped[list['User']] = relationship(
        back_populates="favorited_vacancies",
        secondary="workers_favorited_vacancies"
    )
    tags: Mapped[list['Tag']] = relationship(
        back_populates='vacancies',
        secondary='tags_vacancies'
    )
    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="vacancies",
        secondary="responses"
    )

    def __repr__(self) -> str:
        return self.title


class Responses(Base):
    __tablename__ = 'responses'
    
    resume_id: Mapped[int] = mapped_column(
        ForeignKey('resume.id', ondelete='CASCADE'),
        primary_key=True
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey('vacancy.id', ondelete='CASCADE'),
        primary_key=True
    )
    cover_letter: Mapped[str] = mapped_column(String(3000))
    created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    
    def __repr__(self) -> str:
        return f'response resume#{self.resume_id} - vacancy#{self.vacancy_id}'


class WorkloadsVacancies(Base):
    __tablename__ = "workloads_vacancies"
    
    workload_id: Mapped[int] = mapped_column(
        ForeignKey('workload.id', ondelete='CASCADE'),
        primary_key=True
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey('vacancy.id', ondelete='CASCADE'),
        primary_key=True
    )


class TagsVacancies(Base):
    __tablename__ = 'tags_vacancies'
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tag.id', ondelete='CASCADE'),
        primary_key=True
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey('vacancy.id', ondelete='CASCADE'),
        primary_key=True
    )
    
    

class CitiesResumes(Base):
    __tablename__ = 'cities_resumes'
    city_id: Mapped[int] = mapped_column(
        ForeignKey('city.id', ondelete='CASCADE'),
        primary_key=True
    )
    resume_id: Mapped[int] = mapped_column(
        ForeignKey('resume.id', ondelete='CASCADE'),
        primary_key=True
    )