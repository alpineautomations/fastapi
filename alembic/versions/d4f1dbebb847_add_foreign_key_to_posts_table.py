"""add foreign key to posts table

Revision ID: d4f1dbebb847
Revises: ae0eea670dc5
Create Date: 2026-09-04 11:59:11.318732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4f1dbebb847'
down_revision: Union[str, Sequence[str], None] = 'ae0eea670dc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.droop_contsraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
