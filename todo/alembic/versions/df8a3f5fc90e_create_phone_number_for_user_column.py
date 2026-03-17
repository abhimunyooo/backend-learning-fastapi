"""Create phone number for user column

Revision ID: df8a3f5fc90e
Revises: 
Create Date: 2026-03-16 09:54:13.517793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df8a3f5fc90e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
