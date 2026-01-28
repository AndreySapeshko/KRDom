"""add is_active to materials

Revision ID: fb08a84cc04f
Revises: 2de126004d0c
Create Date: 2026-01-27 07:09:08.415213

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fb08a84cc04f"
down_revision: Union[str, Sequence[str], None] = "2de126004d0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "materials",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.true(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("materials", "is_active")
