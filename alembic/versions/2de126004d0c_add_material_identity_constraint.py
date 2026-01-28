"""add material identity constraint

Revision ID: 2de126004d0c
Revises: 970b9ad14f2b
Create Date: 2026-01-27 06:57:28.601311

"""

from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2de126004d0c"
down_revision: Union[str, Sequence[str], None] = "970b9ad14f2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_unique_constraint(
        "uq_material_identity",
        "materials",
        [
            "width_mm",
            "height_mm",
            "length_mm",
            "kind",
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_material_identity",
        "materials",
        type_="unique",
    )
