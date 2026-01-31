from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, func

from backend.db.base import Base


class Drawing(Base):
    __tablename__ = "drawings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    project_version_id = Column(
        UUID(as_uuid=True),
        ForeignKey("project_versions.id"),
        nullable=False,
    )

    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False, unique=True)

    drawing_type = Column(String(32), nullable=False)  # plan / facade / section
    scale = Column(String(16), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
