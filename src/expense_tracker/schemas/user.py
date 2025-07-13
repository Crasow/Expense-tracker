from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

from expense_tracker.enums import BalanceChangeType


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserRead(UserBase):
    id: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BalanceChangeCreate(BaseModel):
    category_id: int
    amount: float
    description: Optional[str] = None
    date: datetime
    type: BalanceChangeType


class BalanceChangeResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: float
    description: Optional[str]
    date: datetime
    type: BalanceChangeType
    created_at: datetime
