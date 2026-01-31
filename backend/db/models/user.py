from uuid import uuid4

from sqlalchemy import UUID, BigInteger, Boolean, Column, DateTime, Text, func

from backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(Text, unique=True, nullable=True)
    password_hash = Column(Text, nullable=True)

    telegram_id = Column(BigInteger, unique=True, nullable=True)
    username = Column(Text, nullable=True)

    is_active = Column(Boolean, index=True, default=False)
    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
