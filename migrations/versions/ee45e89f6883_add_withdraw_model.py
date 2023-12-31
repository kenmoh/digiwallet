"""add withdraw model

Revision ID: ee45e89f6883
Revises: 3aaf89855e71
Create Date: 2023-09-11 01:37:17.498552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee45e89f6883'
down_revision: Union[str, None] = '3aaf89855e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('withdrawals', sa.Column('user_id', sa.String(), nullable=False))
    op.add_column('withdrawals', sa.Column('wallet_id', sa.String(), nullable=False))
    op.add_column('withdrawals', sa.Column('amount', sa.DECIMAL(), nullable=False))
    op.add_column('withdrawals', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_foreign_key(None, 'withdrawals', 'wallets', ['wallet_id'], ['id'])
    op.create_foreign_key(None, 'withdrawals', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'withdrawals', type_='foreignkey')
    op.drop_constraint(None, 'withdrawals', type_='foreignkey')
    op.drop_column('withdrawals', 'created_at')
    op.drop_column('withdrawals', 'amount')
    op.drop_column('withdrawals', 'wallet_id')
    op.drop_column('withdrawals', 'user_id')
    # ### end Alembic commands ###
