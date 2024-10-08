"""Added new column to SignUp

Revision ID: c888b24ffa48
Revises: 
Create Date: 2024-09-26 19:43:02.470095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c888b24ffa48'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_items_description', table_name='items')
    op.drop_index('ix_items_title', table_name='items')
    op.drop_table('items')
    op.drop_table('signup')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    op.create_table('signup',
    sa.Column('email', sa.VARCHAR(), nullable=False),
    sa.Column('password', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_items_title', 'items', ['title'], unique=False)
    op.create_index('ix_items_description', 'items', ['description'], unique=False)
    # ### end Alembic commands ###
