from sqlalchemy import UUID, Column, DateTime, String

from backend.db.base import Base


class PdfToken(Base):
    __tablename__ = "pdf_tokens"

    token = Column(String, primary_key=True)
    calc_id = Column(UUID(as_uuid=True), nullable=False)
    username = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
