from pydantic import BaseModel
from expense_tracker.enums import CategoryType, RepetitionType
from sqlalchemy.types import Enum
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    type: CategoryType
    color: str
    icon_url: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    color: Optional[str] = None
    icon_url: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    pass
