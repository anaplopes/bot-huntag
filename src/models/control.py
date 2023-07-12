import uuid

from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.models.base import Base


class ControlModel(Base):
    __tablename__ = "download control"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kit_id = Column(Integer, ForeignKey("kits_info.kit_id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())