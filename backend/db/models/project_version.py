from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB

from backend.db.base import Base


class ProjectVersion(Base):
    __tablename__ = "project_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    version = Column(Integer, nullable=False)

    source = Column(String(16), nullable=False)  # llm / user / engineer

    calculation_id = Column(UUID(as_uuid=True), ForeignKey("calculations.id"), nullable=True)

    planning_schema_version = Column(String(16), default="1.0")
    geometry_schema_version = Column(String(16), default="1.0")

    geometry_model = Column(JSONB, nullable=True)

    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint("project_id", "version", name="uq_project_version"),)
