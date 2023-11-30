"""Add some types for mypy

Revision ID: 37a4da024280
Revises: 232924369c05
Create Date: 2023-12-01 01:14:16.067802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37a4da024280'
down_revision: Union[str, None] = '232924369c05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookings', 'room_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
    op.alter_column('bookings', 'room_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###
