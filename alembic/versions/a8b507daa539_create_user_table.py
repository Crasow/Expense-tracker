"""create user table

Revision ID: a8b507daa539
Revises: d7cee4f1c48b
Create Date: 2025-06-28 20:02:50.800722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8b507daa539'
down_revision: Union[str, Sequence[str], None] = 'd7cee4f1c48b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
