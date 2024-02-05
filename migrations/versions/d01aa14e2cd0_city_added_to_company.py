"""City added to company

Revision ID: d01aa14e2cd0
Revises: 0c462142cf8c
Create Date: 2024-01-31 12:04:42.032001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd01aa14e2cd0'
down_revision: Union[str, None] = '0c462142cf8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('url', sa.String(), nullable=True))
    op.add_column('company', sa.Column('email', sa.String(), nullable=True))
    op.drop_column('company', 'url_company')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('url_company', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('company', 'email')
    op.drop_column('company', 'url')
    # ### end Alembic commands ###