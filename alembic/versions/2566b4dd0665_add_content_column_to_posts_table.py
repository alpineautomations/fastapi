"""add content column to posts table

Revision ID: 2566b4dd0665
Revises: 13122af8ff12
Create Date: 2026-09-04 11:42:19.548481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2566b4dd0665'
down_revision: Union[str, Sequence[str], None] = '13122af8ff12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
