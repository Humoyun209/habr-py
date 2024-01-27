"""Initial

Revision ID: 9a43748f555a
Revises: 
Create Date: 2024-01-24 22:02:41.294185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a43748f555a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('workload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_load', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about_company', sa.String(), nullable=False),
    sa.Column('url_company', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('photo', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('about', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('salary', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cities_resumes',
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('city_id', 'resume_id')
    )
    op.create_table('companies_followers',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('company_id', 'user_id')
    )
    op.create_table('tags_resumes',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tag_id', 'resume_id')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('min_salary', sa.Numeric(), nullable=False),
    sa.Column('max_salary', sa.Numeric(), nullable=True),
    sa.Column('about_company', sa.String(), nullable=True),
    sa.Column('candidate_expectation', sa.String(), nullable=True),
    sa.Column('working_conditions', sa.String(), nullable=True),
    sa.Column('bonuses', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workloads_resumes',
    sa.Column('workload_id', sa.Integer(), nullable=False),
    sa.Column('resume_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workload_id'], ['workload.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('workload_id', 'resume_id')
    )
    op.create_table('responses',
    sa.Column('resume_id', sa.String(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('cover_letter', sa.String(length=3000), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('resume_id', 'vacancy_id')
    )
    op.create_table('tags_vacancies',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tag_id', 'vacancy_id')
    )
    op.create_table('workers_favorited_vacancies',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vacancy_id', 'user_id')
    )
    op.create_table('workloads_vacancies',
    sa.Column('workload_id', sa.Integer(), nullable=False),
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancy.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workload_id'], ['workload.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('workload_id', 'vacancy_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workloads_vacancies')
    op.drop_table('workers_favorited_vacancies')
    op.drop_table('tags_vacancies')
    op.drop_table('responses')
    op.drop_table('workloads_resumes')
    op.drop_table('vacancy')
    op.drop_table('tags_resumes')
    op.drop_table('companies_followers')
    op.drop_table('cities_resumes')
    op.drop_table('resume')
    op.drop_table('company')
    op.drop_table('workload')
    op.drop_table('users')
    op.drop_table('tag')
    op.drop_table('city')
    # ### end Alembic commands ###
