import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.models.base import Base


class ControlModel(Base):
    __tablename__ = "download_control"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kit_id = Column(Integer, ForeignKey("kits_info.kit_id"))
    file_name = Column(String(100), nullable=False)
    action = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    detail = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
