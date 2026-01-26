from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB

from backend.db.base import Base


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    source = Column(String(16), nullable=False)  # telegram / web
    calc_version = Column(String(16), nullable=False)  # "1.0"

    input_schema_version = Column(String(16), default="1.0")
    result_schema_version = Column(String(16), default="1.0")

    input_data = Column(JSONB, nullable=False)
    planning_requirements = Column(JSONB, nullable=False)
    calc_result = Column(JSONB, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
