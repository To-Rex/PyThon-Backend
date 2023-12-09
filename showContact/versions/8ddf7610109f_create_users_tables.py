"""create users tables

Revision ID: 8ddf7610109f
Revises: da53c21fea03
Create Date: 2023-12-09 01:31:02.795935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ddf7610109f'
down_revision: Union[str, None] = 'da53c21fea03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
