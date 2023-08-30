"""create posts table

Revision ID: a948bec93b61
Revises: e83465fc7e32
Create Date: 2023-08-27 11:42:08.913065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a948bec93b61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)) 
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
