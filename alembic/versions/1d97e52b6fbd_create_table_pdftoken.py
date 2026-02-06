"""Create table PdfToken

Revision ID: 1d97e52b6fbd
Revises: fb08a84cc04f
Create Date: 2026-02-06 07:03:15.528930

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1d97e52b6fbd"
down_revision: Union[str, Sequence[str], None] = "fb08a84cc04f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "pdf_tokens",
        sa.Column("token", sa.String(128), primary_key=True),
        sa.Column("calc_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String(128), nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("pdf_tokens")
