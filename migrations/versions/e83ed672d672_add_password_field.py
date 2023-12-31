"""add password field

Revision ID: e83ed672d672
Revises: 01860457c5f2
Create Date: 2023-09-10 00:05:11.988822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e83ed672d672'
down_revision: Union[str, None] = '01860457c5f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('topups',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('wallet_address', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('amount', sa.DECIMAL(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallets',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('wallet_address', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('balance', sa.DECIMAL(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'payments', 'wallets', ['wallet_id'], ['id'])
    op.create_foreign_key(None, 'payments', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'transfers', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'transfers', 'wallets', ['wallet_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transfers', type_='foreignkey')
    op.drop_constraint(None, 'transfers', type_='foreignkey')
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.drop_table('wallets')
    op.drop_table('topups')
    op.drop_table('users')
    # ### end Alembic commands ###
