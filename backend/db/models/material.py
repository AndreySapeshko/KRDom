from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Integer, String, func

from backend.db.base import Base


class Material(Base):
    __tablename__ = "materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    section_id = Column(String(64), unique=True, nullable=False)

    width_mm = Column(Integer, nullable=False)
    height_mm = Column(Integer, nullable=False)
    length_mm = Column(Integer, nullable=True)

    kind = Column(String(32), nullable=False, default="GOST 8683 1-2 grade")

    created_at = Column(DateTime, server_default=func.now())
