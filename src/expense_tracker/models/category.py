# models/base_category.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from expense_tracker.enums import CategoryType, RepetitionType
from sqlalchemy.types import Enum

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    color = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, nullable=True)
    # repetition = Column(Enum(RepetitionType), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="categories")