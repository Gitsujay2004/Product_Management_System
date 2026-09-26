"""update session token constraints

Revision ID: 6722683572a5
Revises:
Create Date: 2026-09-26 18:23:51.997568
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6722683572a5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        'sessions',
        'token',
        existing_type=sa.VARCHAR(length=500),
        type_=sa.String(length=5000),
        existing_nullable=False
    )

    op.create_unique_constraint(
        'uq_sessions_token',
        'sessions',
        ['token']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'uq_sessions_token',
        'sessions',
        type_='unique'
    )

    op.alter_column(
        'sessions',
        'token',
        existing_type=sa.String(length=5000),
        type_=sa.VARCHAR(length=500),
        existing_nullable=False
    )