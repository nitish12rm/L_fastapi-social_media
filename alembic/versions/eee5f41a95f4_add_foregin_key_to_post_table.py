"""add_foregin_key to post table

Revision ID: eee5f41a95f4
Revises: ab1a55a4c600
Create Date: 2023-09-21 00:11:28.665393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eee5f41a95f4'
down_revision: Union[str, None] = 'ab1a55a4c600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False)),
    op.create_foreign_key('post_user_fk',source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
