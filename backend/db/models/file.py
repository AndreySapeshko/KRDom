from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, String, Text, func

from backend.db.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    owner_type = Column(String(32), nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=False)

    kind = Column(String(32), nullable=False)
    format = Column(String(8), nullable=False)

    path = Column(Text, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
