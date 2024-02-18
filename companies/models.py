from sqlalchemy import ForeignKey, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    about_company: Mapped[str | None]
    phone: Mapped[str]
    url: Mapped[str]
    email: Mapped[str | None]
    logo: Mapped[str | None]
    banner: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    city_id: Mapped[int | None] = mapped_column(
        ForeignKey("city.id", ondelete="SET NULL")
    )
    city: Mapped["City"] = relationship(back_populates="companies")
    owner: Mapped["User"] = relationship(back_populates="companies")
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="company")
    followers: Mapped[list["User"]] = relationship(
        back_populates="followed_companies", secondary="companies_followers"
    )
    tags: Mapped[list["Tag"]] = relationship(
        back_populates="companies", secondary="tags_companies"
    )

    def __repr__(self) -> str:
        return self.name


class CompaniesFollowers(Base):
    __tablename__ = "companies_followers"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )


class TagsCmpanies(Base):
    __tablename__ = "tags_companies"

    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), primary_key=True)
