"""make length_mm not null

Revision ID: 970b9ad14f2b
Revises: af79965f9297
Create Date: 2026-01-27 06:54:57.118662

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "970b9ad14f2b"
down_revision: Union[str, Sequence[str], None] = "af79965f9297"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "materials",
        "length_mm",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "materials",
        "length_mm",
        existing_type=sa.Integer(),
        nullable=True,
    )
