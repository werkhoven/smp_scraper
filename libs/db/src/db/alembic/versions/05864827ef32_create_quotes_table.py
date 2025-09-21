"""create quotes table

Revision ID: 05864827ef32
Revises: 
Create Date: 2025-09-08 00:09:10.083673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05864827ef32'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'quotes',
        sa.Column(
            'id', sa.UUID, primary_key=True,
            server_default=sa.text('gen_random_uuid()')
        ),
        sa.Column('text', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('tags', sa.String, nullable=False),
        sa.Column(
            'created_at', sa.TIMESTAMP(), nullable=False,
            server_default=sa.func.now()
        ),
        sa.Column(
            'updated_at', sa.TIMESTAMP(), nullable=False,
            server_default=sa.func.now(), onupdate=sa.func.now()
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('quotes')
