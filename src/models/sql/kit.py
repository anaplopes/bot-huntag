import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.models.sql.base import Base


class KitModelSQL(Base):
    __tablename__ = "kits_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kit_id = Column(Integer, nullable=False)
    kit_name = Column(String(100), nullable=False)
    filter_to_kit = Column(String(500))
    kit_creation_date = Column(String(10))
    product_description = Column(String(200))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
