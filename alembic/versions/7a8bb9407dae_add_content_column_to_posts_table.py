"""add content column to posts table

Revision ID: 7a8bb9407dae
Revises: a948bec93b61
Create Date: 2023-08-27 13:57:57.038772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a8bb9407dae'
down_revision = 'a948bec93b61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
