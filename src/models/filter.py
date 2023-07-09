import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.models.base import Base


class FilterModel(Base):
    __tablename__ = "filter"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50), nullable=False)
    subcategory1 = Column(String(100), nullable=False)
    subcategory2 = Column(String(100), nullable=False)
    subcategory3 = Column(String(100), nullable=False)
    subcategory4 = Column(String(100))
    subcategory5 = Column(String(100))
    subcategory6 = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
