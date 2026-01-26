"""initial schema

Revision ID: af79965f9297
Revises:
Create Date: 2026-01-25 08:49:34.689753

"""

from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import ForeignKey, func

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "af79965f9297"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("email", sa.Text(), unique=True),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.Column("telegram_id", sa.BigInteger(), unique=True, nullable=True),
        sa.Column("username", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.true(), index=True),
        sa.Column("is_admin", sa.Boolean, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "materials",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("section_id", sa.String(64), unique=True, nullable=False),
        sa.Column("width_mm", sa.Integer, nullable=False),
        sa.Column("height_mm", sa.Integer, nullable=False),
        sa.Column("length_mm", sa.Integer, nullable=True),
        sa.Column("kind", sa.String(32), nullable=False, default="GOST 8683 1-2 grade"),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "calculations",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("user_id", sa.UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
        sa.Column("source", sa.String(16), nullable=False),
        sa.Column("calc_version", sa.String(16), nullable=False),  # "1.0"
        sa.Column("input_schema_version", sa.String(16), default="1.0"),
        sa.Column("result_schema_version", sa.String(16), default="1.0"),
        sa.Column("input_data", sa.JSONB, nullable=False),
        sa.Column("planning_requirements", sa.JSONB, nullable=False),
        sa.Column("calc_result", sa.JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("user_id", sa.UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
        sa.Column(
            "parent_project_id", sa.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=True, default=None
        ),
        sa.Column("calculation_id", sa.UUID(as_uuid=True), ForeignKey("calculations.id"), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, default="draft"),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "project_versions",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("project_id", sa.UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("source", sa.String(16), nullable=False),
        sa.Column("calculation_id", sa.UUID(as_uuid=True), ForeignKey("calculations.id"), nullable=True),
        sa.Column("planning_schema_version", sa.String(16), default="1.0"),
        sa.Column("geometry_schema_version", sa.String(16), default="1.0"),
        sa.Column("geometry_model", sa.JSONB, nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
        sa.UniqueConstraint("project_id", "version", name="uq_project_version"),
    )

    op.create_table(
        "files",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("owner_type", sa.String(32), nullable=False),
        sa.Column("owner_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("format", sa.String(8), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )

    op.create_table(
        "drawings",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("project_version_id", sa.UUID(as_uuid=True), ForeignKey("project_versions.id"), nullable=False),
        sa.Column("file_id", sa.UUID(as_uuid=True), ForeignKey("files.id"), nullable=False, unique=True),
        sa.Column("drawing_type", sa.String(32), nullable=False),
        sa.Column("scale", sa.String(16), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("drawings")
    op.drop_table("files")
    op.drop_table("project_versions")
    op.drop_table("projects")
    op.drop_table("calculations")
    op.drop_table("materials")
    op.drop_table("users")
