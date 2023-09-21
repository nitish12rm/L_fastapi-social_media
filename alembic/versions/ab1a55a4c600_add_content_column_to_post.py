"""add_content_column_to_post

Revision ID: ab1a55a4c600
Revises: 1ab23ba064ce
Create Date: 2023-09-21 00:07:13.428759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab1a55a4c600'
down_revision: Union[str, None] = '1ab23ba064ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','column')
    pass
