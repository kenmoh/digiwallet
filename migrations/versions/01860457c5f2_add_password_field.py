"""add password field

Revision ID: 01860457c5f2
Revises: b8b620c5be6a
Create Date: 2023-09-09 23:45:23.148376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01860457c5f2'
down_revision: Union[str, None] = 'b8b620c5be6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topups', sa.Column('password', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topups', 'password')
    # ### end Alembic commands ###
