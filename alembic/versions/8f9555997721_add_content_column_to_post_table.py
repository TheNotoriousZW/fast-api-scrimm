"""add content column to post table

Revision ID: 8f9555997721
Revises: 058d2a094487
Create Date: 2023-12-13 00:50:47.606387

"""
from tokenize import String
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f9555997721'
down_revision: Union[str, None] = '058d2a094487'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False), )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
