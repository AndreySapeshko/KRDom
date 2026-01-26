from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, func

from backend.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    parent_project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True, default=None)

    calculation_id = Column(UUID(as_uuid=True), ForeignKey("calculations.id"), nullable=True)

    status = Column(String(32), nullable=False, default="draft")

    created_at = Column(DateTime, server_default=func.now())
