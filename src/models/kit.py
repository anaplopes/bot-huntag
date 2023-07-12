import uuid

from sqlalchemy import Column, DateTime, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.models.base import Base


class KitModel(Base):
    __tablename__ = "kits_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kit_id = Column(Integer)
    kit_name = Column(String(100))
    filter_to_kit = Column(String(500))
    kit_creation_date = Column(Date)
    product_description = Column(String(200))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
