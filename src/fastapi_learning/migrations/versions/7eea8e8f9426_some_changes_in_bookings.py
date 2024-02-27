"""Some changes in bookings

Revision ID: 7eea8e8f9426
Revises: 847fb887adfd
Create Date: 2024-02-20 23:31:02.919454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7eea8e8f9426'
down_revision: Union[str, None] = '847fb887adfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
