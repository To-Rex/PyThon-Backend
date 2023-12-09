"""create student table

Revision ID: da53c21fea03
Revises: 91596e08eceb
Create Date: 2023-12-09 01:28:10.445757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da53c21fea03'
down_revision: Union[str, None] = '91596e08eceb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
