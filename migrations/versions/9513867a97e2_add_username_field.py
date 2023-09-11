"""add username field

Revision ID: 9513867a97e2
Revises: e83ed672d672
Create Date: 2023-09-10 01:32:20.446312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9513867a97e2'
down_revision: Union[str, None] = 'e83ed672d672'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'payments', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'payments', 'wallets', ['wallet_id'], ['id'])
    op.add_column('transfers', sa.Column('username', sa.String(), nullable=False))
    op.create_foreign_key(None, 'transfers', 'wallets', ['wallet_id'], ['id'])
    op.create_foreign_key(None, 'transfers', 'users', ['user_id'], ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'transfers', type_='foreignkey')
    op.drop_constraint(None, 'transfers', type_='foreignkey')
    op.drop_column('transfers', 'username')
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.drop_constraint(None, 'payments', type_='foreignkey')
    # ### end Alembic commands ###
