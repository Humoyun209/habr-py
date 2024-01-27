from sqlalchemy import ForeignKey, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Company(Base):
    __tablename__ = 'company'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    about_company: Mapped[str]
    url_company: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped['User'] = relationship(back_populates='companies')
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates='company')
    followers: Mapped[list["User"]] = relationship(
        back_populates='followed_companies', 
        secondary='companies_followers'
    )
    
    def __repr__(self) -> str:
        return self.name


class CompaniesFollowers(Base):
    __tablename__ = 'companies_followers'
    
    company_id: Mapped[int] = mapped_column(
        ForeignKey('company.id', ondelete='CASCADE'),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    

class WorkLoad(Base):
    __tablename__ = 'workload'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    work_load: Mapped[str] = mapped_column(String(100))
    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="workloads",
        secondary="workloads_resumes"
    )
    vacancies: Mapped[list["Vacancy"]] = relationship(
        back_populates="workloads",
        secondary="workloads_vacancies"
    )
    
    def __repr__(self) -> str:
        return f'Условие - {self.work_load}'